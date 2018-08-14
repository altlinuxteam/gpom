from configparser import SafeConfigParser
from cses.cse import load as cse_load
from common import error, warning, info, debug
#import fnmatch
#import importlib

class GPE(object):
    def __init__(self, gpo, ini_path, gpo_path):
        self.cses = []
        self.ini_path = ini_path
        self.gpo_path = gpo_path
        self.gpo = gpo
        self.cses = []
        self.parse()


    def parse(self):
        conf = SafeConfigParser()
        conf.read(self.ini_path)
        general = conf['General']
        for (s, v) in general.iteritems():
            is_machine_policy = (s == 'machineextensionversions')
            a = [ x[1:] for x in general[s].split(']') if x ]
            for z in a:
                b = [ x[1:] for x in z.split('}') ]
                (version, guids) = (b[-1], b[:-1])
                cse = cse_load(self.gpo, guids[0], is_machine_policy)
                cse.parse(self.gpo_path)
                print(self.gpo_path)
                self.cses.append({'guids': guids,
                                  'version': version,
                                  'cse': cse
                })
