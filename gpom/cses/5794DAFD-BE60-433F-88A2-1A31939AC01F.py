from gpom.cses import CSE
#from gpom.gpos import state
import xmltodict


class CSEImpl(CSE):
    def __init__(self, gpo):
        self.name = 'Preference_CSE_GUID_Drives'
        self.guid = '5794DAFD-BE60-433F-88A2-1A31939AC01F'
        self.gpo = gpo
        self.drives = []
        self.pref_files = [
            ('/User/Preferences/Drives/Drives.xml', self.parse_drives)
        ]


    def parse_drives(self, path):
        with open(path, 'r') as f:
            d = xmltodict.parse(f.read())
            self.drives = [ self.parse_drive(x) for x in d['Drives']['Drive'] ]


    def parse_drive(self, d):
        res = {'clsid': d['@clsid'],
               'name': d['@name'],
               'status': d['@status'],
               'image': d['@image'],
               'chanded': d['@changed'],
               'uid': d['@uid'],
               'action': d['Properties']['@action'],
               'thisDrive': d['Properties']['@thisDrive'],
               'allDrives': d['Properties']['@allDrives'],
               'userName': d['Properties']['@userName'],
               'path': d['Properties']['@path'],
               'label': d['Properties']['@label'],
               'persistent': d['Properties']['@persistent'],
               'useLetter': d['Properties']['@useLetter'],
               'letter': d['Properties']['@letter']
        }
        return res


    def get_local_state(self):
        print("local state")
        try:
            return state['gpo'][self.gpo.name]['policies']['cse'][self.guid]
        except KeyError:
            return None


    def pol2state(self):
        pass


    def __compare__(self, local_state, gpo_state):
        pass
