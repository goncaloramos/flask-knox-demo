from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from azure.appconfiguration.provider import AzureAppConfigurationProvider, SettingSelector
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

connection_string = os.environ.get("AZURE_APPCONFIG_CONNECTION_STRING")
kv_name = os.environ.get("KEY_VAULT_NAME")

KVUri = f"https://knox-kv.vault.azure.net"

az_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
az_client = SecretClient(vault_url=KVUri, credential=az_credential)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       if name == 'vault':
           print('Request for hello page received with name=%s' % name)
           print('Retrieving secrets from Key Vault')
           retrieved_kv_secret = az_client.get_secret("hello-kv")
           print("secret " + retrieved_secret.value)
           return render_template('hello.html', name=retrieved_kv_secret.value)
       else:
           print('Request for hello page received with name=%s' % name)
           return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       # Connect to Azure App Configuration using a connection string.
       az_configapp = AzureAppConfigurationProvider.load(connection_string=connection_string)
       return render_template('hello.html', name = az_configapp['hello'])
       #return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()