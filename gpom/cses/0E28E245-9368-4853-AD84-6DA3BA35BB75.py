from gpom.cses import CSE
import xmltodict


class CSEImpl(CSE):
    def __init__(self, gpo):
        self.name = 'Preference CSE GUID Environment Variables'
        self.guid = '0E28E245-9368-4853-AD84-6DA3BA35BB75'
        self.gpo = gpo
        self.evs = []
        self.pref_files = [
            ('/User/Preferences/EnvironmentVariables/EnvironmentVariables.xml', self.parse_evs)
        ]


    def parse_evs(self, path):
        with open(path, 'r') as f:
            d = xmltodict.parse(f.read())
            self.evs = [ self.parse_ev(x) for x in d['EnvironmentVariables']['EnvironmentVariable'] ]


    def parse_ev(self, d):
        res = {'clsid': d['@clsid'],
               'name': d['@name'],
               'status': d['@status'],
               'image': d['@image'],
               'chanded': d['@changed'],
               'uid': d['@uid'],
               'action': d['Properties']['@action'],
               'prop_name': d['Properties']['@name'],
               'value': d['Properties']['@value'],
               'user': d['Properties']['@user'],
               'partial': d['Properties']['@partial']
        }
        return res
