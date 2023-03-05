from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from azure.appconfiguration.provider import AzureAppConfigurationProvider, SettingSelector
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

#connection_string = os.environ.get("AZURE_APPCONFIG_CONNECTION_STRING")
connection_string = "Endpoint=https://app-config-knox.azconfig.io;Id=5JOl-l4-s0:c/gcBEecO/MMtBPwNlvJ;Secret=TZXxT3KqEd5Wi9dsDeySDgXN1tTcIccBNn++QAoT8DM="

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
           az_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

           az_configapp = AzureAppConfigurationProvider.load(connection_string=connection_string)
           kv_name = az_configapp['vault-name']
           print("kv name: " + kv_name)
           KVUri = f"https://{kv_name}.vault.azure.net"
           print("kv uri: " + KVUri)
           az_client = SecretClient(vault_url=KVUri, credential=az_credential)
           retrieved_kv_secret = az_client.get_secret("hello-kv")
           print("secret " + retrieved_kv_secret.value)
           return render_template('hello.html', name=retrieved_kv_secret.value)
           #return render_template('hello.html', name=kv_name)
       else:
           print('Request for hello page received with name=%s' % name)
           return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.debug = True
   app.run()