import os
import random
import uuid
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from haikunator import Haikunator
from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint
from msrestazure.azure_active_directory import UserPassCredentials
from azure.profiles import KnownProfiles

haikunator = Haikunator()

# Azure Datacenter
LOCATION = 'local'

# Resource Group
postfix = random.randint(100, 500)
GROUP_NAME = 'azure-sample-group-virtual-machines{}'.format(postfix)

# Network
VNET_NAME = 'azure-sample-vnet{}'.format(postfix)
SUBNET_NAME = 'azure-sample-subnet{}'.format(postfix)

# VM
OS_DISK_NAME = 'azure-sample-osdisk{}'.format(postfix)
STORAGE_ACCOUNT_NAME = haikunator.haikunate(delimiter='')

IP_CONFIG_NAME = 'azure-sample-ip-config{}'.format(postfix)
NIC_NAME = 'azure-sample-nic{}'.format(postfix)
USERNAME = 'userlogin'
PASSWORD = str(uuid.uuid4())
VM_NAME = 'VmName{}'.format(postfix)

VM_REFERENCE = {
    'linux': {
        'publisher': 'Canonical',
        'offer': 'UbuntuServer',
        'sku': '16.04-LTS',
        'version': 'latest'
    },
    'windows': {
        'publisher': 'MicrosoftWindowsServer',
        'offer': 'WindowsServer',
        'sku': '2012-R2-Datacenter',
        'version': '1.0.0'
    }
}

# Manage resources and resource groups - create, update and delete a resource group,
# deploy a solution into a resource group, export an ARM template. Create, read, update
# and delete a resource
#
# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
# ARM_ENDPOINT: with your Azure Resource Manager Endpoint
#
def run_example():
    """Resource Group management example."""
    #
    # Create all clients with an Application (service principal) token provider
    #
    mystack_cloud = get_cloud_from_metadata_endpoint(os.environ['ARM_ENDPOINT'])

    # Set Storage Endpoint suffix
    arm_url = mystack_cloud.endpoints.resource_manager
    storage_endpoint_suffix = arm_url.replace(arm_url.split(".")[0], "").strip('./')

    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID',
        '11111111-1111-1111-1111-111111111111') # your Azure Subscription Id
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID'],
        cloud_environment=mystack_cloud
    )

    # By Default, use AzureStack supported profile
    KnownProfiles.default.use(KnownProfiles.v2017_03_09_profile)

    resource_client = ResourceManagementClient(credentials, subscription_id, base_url=mystack_cloud.endpoints.resource_manager)
    compute_client = ComputeManagementClient(credentials, subscription_id, base_url=mystack_cloud.endpoints.resource_manager)
    storage_client = StorageManagementClient(credentials, subscription_id, base_url=mystack_cloud.endpoints.resource_manager)
    network_client = NetworkManagementClient(credentials, subscription_id, base_url=mystack_cloud.endpoints.resource_manager)

    ###########
    # Prepare #
    ###########

    # Create Resource group
    print('\nCreate Resource Group')
    resource_client.resource_groups.create_or_update(GROUP_NAME, {'location':LOCATION})

    # Create a storage account
    print('\nCreate a storage account')
    storage_async_operation = storage_client.storage_accounts.create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            'sku': {'name': 'standard_lrs'},
            'kind': 'storage',
            'location': LOCATION
        }
    )
    storage_async_operation.wait()

    # Create a NIC
    nic = create_nic(network_client)

    #############
    # VM Sample #
    #############

    # Create Linux VM
    print('\nCreating Linux Virtual Machine')
    vm_parameters = create_vm_parameters(nic.id, VM_REFERENCE['linux'], storage_endpoint_suffix)
    async_vm_creation = compute_client.virtual_machines.create_or_update(
        GROUP_NAME, VM_NAME, vm_parameters)
    async_vm_creation.wait()

    # Tag the VM
    print('\nTag Virtual Machine')
    async_vm_update = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        {
            'location': LOCATION,
            'tags': {
                'who-rocks': 'python',
                'where': 'on azure'
            }
        }
    )
    async_vm_update.wait()

    # Attach data disk
    print('\nAttach Data Disk')
    async_vm_update = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        {
            'location': LOCATION,
            'storage_profile': {
                'data_disks': [{
                    'name': 'mydatadisk1',
                    'disk_size_gb': 1,
                    'lun': 0,
                    'vhd': {
                        'uri' : "https://{}.blob.{}/vhds/mydatadisk1.vhd".format(
                            STORAGE_ACCOUNT_NAME, storage_endpoint_suffix)
                    },
                    'create_option': 'Empty'
                }]
            }
        }
    )
    async_vm_update.wait()

    # Get the virtual machine by name
    print('\nGet Virtual Machine by Name')
    virtual_machine = compute_client.virtual_machines.get(
        GROUP_NAME,
        VM_NAME
    )

    # Detach data disk
    print('\nDetach Data Disk')
    data_disks = virtual_machine.storage_profile.data_disks
    data_disks[:] = [disk for disk in data_disks if disk.name != 'mydatadisk1']
    async_vm_update = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        virtual_machine
    )
    virtual_machine = async_vm_update.result()
    
    # Deallocating the VM (resize prepare)
    print('\nDeallocating the VM (resize prepare)')
    async_vm_deallocate = compute_client.virtual_machines.deallocate(GROUP_NAME, VM_NAME)
    async_vm_deallocate.wait()

    # Update OS disk size by 10Gb
    print('\nUpdate OS disk size')
    # Server is not returning the OS Disk size (None), possible bug in server
    if not virtual_machine.storage_profile.os_disk.disk_size_gb:
        print("\tServer is not returning the OS disk size, possible bug in the server?")
        print("\tAssuming that the OS disk size is 256 GB")
        virtual_machine.storage_profile.os_disk.disk_size_gb = 256

    virtual_machine.storage_profile.os_disk.disk_size_gb += 10
    async_vm_update = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        virtual_machine
    )
    virtual_machine = async_vm_update.result()

    # Start the VM
    print('\nStart VM')
    async_vm_start = compute_client.virtual_machines.start(GROUP_NAME, VM_NAME)
    async_vm_start.wait()

    # Restart the VM
    print('\nRestart VM')
    async_vm_restart = compute_client.virtual_machines.restart(GROUP_NAME, VM_NAME)
    async_vm_restart.wait()

    # Stop the VM
    print('\nStop VM')
    async_vm_stop = compute_client.virtual_machines.power_off(GROUP_NAME, VM_NAME)
    async_vm_stop.wait()

    # List VMs in subscription
    print('\nList VMs in subscription')
    for vm in compute_client.virtual_machines.list_all():
        print("\tVM: {}".format(vm.name))

    # List VM in resource group
    print('\nList VMs in resource group')
    for vm in compute_client.virtual_machines.list(GROUP_NAME):
        print("\tVM: {}".format(vm.name))

    # Delete VM
    print('\nDelete VM')
    async_vm_delete = compute_client.virtual_machines.delete(GROUP_NAME, VM_NAME)
    async_vm_delete.wait()

    # Create Windows VM
    print('\nCreating Windows Virtual Machine')
    # Recycling NIC of previous VM
    vm_parameters = create_vm_parameters(nic.id, VM_REFERENCE['windows'], storage_endpoint_suffix)
    async_vm_creation = compute_client.virtual_machines.create_or_update(
        GROUP_NAME, VM_NAME, vm_parameters)
    async_vm_creation.wait()

    input("Press enter to delete this Resource Group.")

    # Delete Resource group and everything in it
    print('\nDelete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))

def create_nic(network_client):
    """Create a Network Interface for a VM.
    """
    # Create VNet
    print('\nCreate Vnet')
    async_vnet_creation = network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        {
            'location': LOCATION,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )
    async_vnet_creation.wait()

    # Create Subnet
    print('\nCreate Subnet')
    async_subnet_creation = network_client.subnets.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    )
    subnet_info = async_subnet_creation.result()

    # Create NIC
    print('\nCreate NIC')
    async_nic_creation = network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        NIC_NAME,
        {
            'location': LOCATION,
            'ip_configurations': [{
                'name': IP_CONFIG_NAME,
                'subnet': {
                    'id': subnet_info.id
                }
            }]
        }
    )
    return async_nic_creation.result()

def create_vm_parameters(nic_id, vm_reference, storage_endpoint_suffix):
    """Create the VM parameters structure.
    """

    return {
        'location': LOCATION,
        'os_profile': {
            'computer_name': VM_NAME,
            'admin_username': USERNAME,
            'admin_password': PASSWORD
        },
        'hardware_profile': {
            'vm_size': 'Standard_A1'
        },
        'storage_profile': {
            'image_reference': {
                'publisher': vm_reference['publisher'],
                'offer': vm_reference['offer'],
                'sku': vm_reference['sku'],
                'version': vm_reference['version']
            },
            'os_disk': {
                'name': OS_DISK_NAME,
                'caching': 'None',
                'create_option': 'fromImage',
                'vhd': {
                    'uri': 'https://{}.blob.{}/vhds/{}.vhd'.format(
                        STORAGE_ACCOUNT_NAME, storage_endpoint_suffix , VM_NAME+haikunator.haikunate())
                }
            },
        },
        'network_profile': {
            'network_interfaces': [{
                'id': nic_id,
            }]
        },
    }


if __name__ == "__main__":
    run_example()
