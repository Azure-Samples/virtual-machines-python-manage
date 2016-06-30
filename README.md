---
services: virtual-machines
platforms: java
author: lmazuel
---

# Azure Virtual Machines Management Samples - Python
These samples demonstrate how to perform common management tasks with Microsoft Azure Virtual Machines using Python. The code examples provided show how to do the following:

- Create a virtual machine
- Start a virtual machine
- Stop a virtual machine
- Restart a virtual machine
- Update a virtual machine
	- Expand a drive
	- Tag a virtual machine
	- Attach data disks
	- Detach data disks
- List virtual machines
- Delete a virtual machine.


## Running this sample
1. If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, and 3.5.

2. We recommend to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. Install and initialize the virtual environment with:

    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

3. Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/virtual-machines-python-manage.git
    ```

4. Install the dependencies using pip.

    ```
    cd virtual-machines-python-manage
    pip install -r requirements.txt
    ```

5. Create an Azure service principal either through
[Azure CLI](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/),
[PowerShell](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [the portal](http://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/).

6. Fill in and export these environment variables into your current shell. 

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    ```

7. Run the sample.

    ```
    python example.py
    ```
    
## More information

Here are some helpful links:

- [Azure Python Development Center] (https://azure.microsoft.com/develop/python/)
- [Azure Virtual Machines documentation](https://azure.microsoft.com/services/virtual-machines/)
- [Learning Path for Virtual Machines](https://azure.microsoft.com/documentation/learning-paths/virtual-machines/)

If you don't have a Microsoft Azure subscription you can get a FREE trial account [here](http://go.microsoft.com/fwlink/?LinkId=330212).

---

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

