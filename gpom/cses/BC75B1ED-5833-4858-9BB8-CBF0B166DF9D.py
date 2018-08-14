from gpom.cses import CSE
import xmltodict


class CSEImpl(CSE):
    def __init__(self, gpo, is_machine_policy):
        super(CSEImpl, self).__init__()
        self.name = 'Printers CSE'
        self.guid = 'BC75B1ED-5833-4858-9BB8-CBF0B166DF9D'
        self.gpo = gpo
        self.evs = []
        self.is_machine_policy = is_machine_policy
        self.pref_files = [
            ('Preferences/Printers/Printers.xml', self.parse_printers)
        ]


    def parse_printers(self, path):
        with open(path, 'r') as f:
            d = xmltodict.parse(f.read())
#            self.evs = [ self.parse_ev(x) for x in d['EnvironmentVariables']['EnvironmentVariable'] ]


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
