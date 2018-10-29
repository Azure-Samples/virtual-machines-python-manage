---
services: virtual-machines
platforms: python
author: lmazuel
---

# Azure Virtual Machines Management Samples - Python
These samples demonstrate how to perform common management tasks
with Microsoft Azure Virtual Machines
using the Azure SDK for Python.
The code provided shows how to do the following:

- Create virtual machines:
    - Create a Linux virtual machine
    - Create a Windows virtual machine
- Update a virtual machine:
	- Expand a drive
	- Tag a virtual machine
	- Attach data disks
	- Detach data disks
- Operate a virtual machine:
    - Start a virtual machine
    - Stop a virtual machine
    - Restart a virtual machine
- List virtual machines
- Delete a virtual machine

To see the code to perform these operations,
check out the `run_example()` function in [example.py](example.py).
Each operation is clearly labeled with a comment and a print function.
The examples are not necessarily in the order shown in the above list.


## Running this sample
1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, 3.5 and 3.6.

2.  We recommend that you use a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
    to run this example, but it's not mandatory.
    Install and initialize the virtual environment with:

    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

3.  Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/virtual-machines-python-manage.git
    ```

4.  Install the dependencies using pip.

    ```
    cd virtual-machines-python-manage
    pip install -r requirements.txt
    ```

5.  Create an Azure service principal either through
[Azure CLI](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/),
[PowerShell](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [the portal](http://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/).

    Retrieve the application ID (a.k.a. client ID),
    authentication key (a.k.a. client secret),
    tenant ID and subscription ID from the Azure portal for use
    in the next step.
    [This document](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal#get-application-id-and-authentication-key)
    describes where to find them (besides the subscription ID,
    which is in the "Overview" section of the "Subscriptions" blade.)

6.  Fill in and export these environment variables into your current shell. 

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    ```

7.  Run the sample.

    ```
    python example.py
    ```

## Notes

### Retrieving a VM's OS disk

You may be tempted to try to retrieve a VM's OS disk by using
`virtual_machine.storage_profile.os_disk`.
In some cases, this may do what you want,
but be aware that it gives you an `OSDisk` object.
In order to update the OS Disk's size, as `example.py` does,
you need not an `OSDisk` object but a `Disk` object.
`example.py` gets the `Disk` object with the following:

```python
os_disk_name = virtual_machine.storage_profile.os_disk.name
os_disk = compute_client.disks.get(GROUP_NAME, os_disk_name)
```
    
## More information

Here are some helpful links:

- [Azure Python Development Center](https://azure.microsoft.com/develop/python/)
- [Azure Virtual Machines documentation](https://azure.microsoft.com/services/virtual-machines/)
- [Learning Path for Virtual Machines](https://docs.microsoft.com/learn/modules/intro-to-azure-virtual-machines/index)

If you don't have a Microsoft Azure subscription you can get a FREE trial account [here](http://go.microsoft.com/fwlink/?LinkId=330212).

---

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

