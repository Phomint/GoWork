import gowork
import json
import os
import pathlib
import codecs


class Credentials:
    def __init__(self):
        self._root = '/'.join(gowork.__file__.split('/')[:-1]+['safe', 'secret_keys.json'])
        self.creds = {}

    def insert(self, name: str, connector: str, credentials: dict):
        name = name.lower()
        connector = connector.lower()

        self._load()
        if connector not in self.creds.keys():
            self.creds[connector] = {}
        self.creds[connector][name] = credentials
        with open(self._root, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.creds, indent=4))

    def select(self, connector: str, name: str):
        name = name.lower()
        connector = connector.lower()

        self._load()
        if connector in self.creds:
            if name in self.creds[connector]:
                return self.creds[connector][name]
            else:
                print('Name connection not found')
        print('Connector not found')

    def _load(self):
        if os.path.exists(self._root):
            with open(self._root, 'r', encoding='utf-8') as file:
                self.creds = json.load(file)


