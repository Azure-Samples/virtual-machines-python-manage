# virtual-machines-python-manage
An example illustrating how to use Python to manage your Azure Virtual Machines

## Running this sample
1. If you don't already have it, [install Python](https://www.python.org/downloads/).

2. We recommend to use a [virtual environnement](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. You can initialize a virtualenv this way:

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

6. Export these environment variables into your current shell. 

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

## About the code
Coming soon...
## More information
Coming soon...