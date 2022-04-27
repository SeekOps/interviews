'''
This class of functions is used to make queries from Kowalski
from a local machine. You must first authenticate with `az login`
to use these functions. See the README for more details on how
to install the Azure CLI if you haven't done so.

Author: Kyle Dawson
Copyright: SeekOps, Inc.
Date: 14-April-2022
'''
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
import os, logging
import pandas as pd
from sqlalchemy import create_engine

class AuthException(Exception):
    ''' catches authentication errors '''
    def __init__(self,Exception: str):
        print(Exception)
        logging.error("Authentication Failed, run `az login` in a separate terminal window")

class KowalskiConnect:

    def __init__(self):
        return

    @staticmethod
    def get_secrets(vault_uri=None):
        
        credential = AzureCliCredential()
        
        if vault_uri:
            pass
        else:
            vault_uri  = os.environ.get("KEY_VAULT_URL","https://kowalski.vault.azure.net/")

        secret_client = SecretClient(vault_url=vault_uri, credential=credential)
        keys = {}
        try:
            for iter in secret_client.list_properties_of_secrets():
                keys.update({iter.name:secret_client.get_secret(name=iter.name).value})
            return keys
        except Exception as e:
            AuthException(e)
            return
    
    def connect(self):
        ''' connecting to the database '''
        keys     = self.get_secrets()
        uri_base = 'postgresql' 
        uri      = (f"{uri_base}://{keys['USER']}:{keys['PASSWORD']}@"
                    f"{keys['HOST']}:{keys['PORT']}/{keys['DATABASE']}")
        engine = create_engine(uri)
        return engine

class queryKowalski(KowalskiConnect):
    ''' 
    use this class to run queries on Kowalski 
    try this test query:
    query = """ select * from api_measurement limit 1 """
    '''    
    
    @staticmethod
    def get_data(query: str):
        # opening connection
        conn  = KowalskiConnect().connect()
        
        # getting data
        data  = pd.read_sql_query(query,conn)
        
        # closing connection
        conn  = None
        return data
