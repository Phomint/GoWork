import gowork
import json
import os
import base64
import platform
import pathlib


class Credentials:
    def __init__(self):
        self.__platform = '\\' if platform.system().__str__() == 'Windows' else '/'
        self.__root = self.__platform.join(gowork.__file__.split(self.__platform)[:-1] + ['safe', 'secret_keys.json'])
        self.__creds = {}
        self.__project = pathlib.Path().resolve().__str__()

    def insert(self, name: str, connector: str, credentials: dict, encode=[]):
        name = name.lower()
        connector = connector.lower()

        self.__load()
        if connector not in self.__creds.keys():
            self.__creds[connector] = {}
        if len(encode) > 0:
            credentials = self.__encode(credentials, encode)
        self.__creds[connector][name] = credentials
        with open(self.__root, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.__creds, indent=4))

    def export_credentials(self):
        try:
            os.popen(f'cp {self.__root} {self.__project + self.__platform + "gowork_secret_keys.json"}')
            print('Exported successfully')
        except:
            print('Exported failed')

    def import_credentials(self, path='.'):
        try:
            os.popen(f'cp {self.__project + self.__platform + path + self.__platform + "gowork_secret_keys.json"} {self.__root}')
            print('Imported successfully')
        except:
            print('File not found')

    def get_credentials(self) -> dict:
        self.__load()
        creds = {}
        for k in self.__creds.keys():
            for sk in self.__creds[k].keys():
                creds[k] = sk
        return creds

    def select(self, connector: str, name: str):
        name = name.lower()
        connector = connector.lower()

        self.__load()
        if connector in self.__creds:
            if name in self.__creds[connector]:
                return self.__creds[connector][name]
            else:
                print('Name connection not found')
        print('Connector not found')

    def __load(self):
        if os.path.exists(self.__root):
            with open(self.__root, 'r', encoding='utf-8') as file:
                self.__creds = json.load(file)

    def __encode(self, credentials: dict, keys: list):
        for key in keys:
            credentials[key] = {'encode': base64.b64encode(credentials[key].encode('utf-8')).decode('utf-8')}
        return credentials


