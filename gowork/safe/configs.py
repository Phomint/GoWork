import gowork
import json
import os
import pathlib
import codecs
import base64

class Credentials:
    def __init__(self):
        self.__root = '/'.join(gowork.__file__.split('/')[:-1]+['safe', 'secret_keys.json'])
        self.creds = {}

    def insert(self, name: str, connector: str, credentials: dict, encode=[]):
        name = name.lower()
        connector = connector.lower()

        self.__load()
        if connector not in self.creds.keys():
            self.creds[connector] = {}
        if len(encode) > 0:
            credentials = self.__encode(credentials, encode)
        self.creds[connector][name] = credentials
        with open(self.__root, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.creds, indent=4))

    def select(self, connector: str, name: str):
        name = name.lower()
        connector = connector.lower()

        self.__load()
        if connector in self.creds:
            if name in self.creds[connector]:
                return self.creds[connector][name]
            else:
                print('Name connection not found')
        print('Connector not found')

    def __load(self):
        if os.path.exists(self.__root):
            with open(self.__root, 'r', encoding='utf-8') as file:
                self.creds = json.load(file)

    def __encode(self, credentials: dict, keys: list):
        for key in keys:
            credentials[key] = {'encode': base64.b64encode(credentials[key].encode('utf-8')).decode('utf-8')}
        return credentials
