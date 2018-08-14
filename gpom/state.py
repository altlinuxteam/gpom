from common import error, warning, info, debug
import os
import json


class State(object):
    def __init__(self, db_path=None, init=False, force=False):
        self.state_file = "state.json"
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = config['Default']['db_path']

        self.state_file_path = "%s/%s" % (self.db_path, self.state_file)

        debug("db_path is %s" % self.db_path)
        if not os.path.isdir(self.db_path) and not init:
            raise RuntimeError("Directory %s not found. Please init it first via `init` method" % db_path)

        if not os.path.isfile(self.state_file_path) and not init:
            raise RuntimeError("Cannot load %s/state.json. Please init it first via `init` method" % db_path)

        if init:
            self.init(force)

        self.load()


    def init(self, force=False):
        if os.path.isdir(self.db_path) and not force:
            raise RuntimeError("%s is already exists. use `force` flag to overwrite" % self.db_path)
        elif os.path.isdir(self.db_path) and force:
            shutil.rmtree(self.db_path)

        os.makedirs(self.db_path)

        self.state = {'last_attemp': 0,
                      'last_success': 0
        }
        self.save()


    def load(self):
        with open("%s/%s" % (self.db_path, self.state_file)) as f:
            self.state = json.load(f)


    def save(self):
        with open(self.state_file_path, 'w') as f:
            f.write(json.dumps(self.state))


    def state(self):
        return self.state


    def get(self, cont, key):
        if cont not in self.state.keys():
            return None
        if key not in self.state[cont].keys():
            return None

        return self.state[cont][key]


    def set(self, cont, key, val):
        new = {}
        if cont in self.state.keys():
            new = self.state[cont]
        new[key] = val
        self.state[cont] = new
        self.save()


    def __getitem__(self, key):
        return self.state[key]
