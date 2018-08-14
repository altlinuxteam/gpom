from policy import Policy
from common import error, warning, info, debug
import os
from itertools import chain
from configparser import SafeConfigParser
import fnmatch
import importlib
from gpe import GPE


polmap = {'Software/Microsoft/Windows/CurrentVersion/Policies/System':
          ['Wallpaper',
           'WallpaperStyle'
          ],
          'Software/Policies/Microsoft/Windows NT/Printers': []
}


class GPO(object):
    def __init__(self, path, name, whenChanged=None):
        self.policies = []
        self.path = path
        self.whenChanged = whenChanged
        self.name = name
        self.guid = self.path.split('/')[-1]
        self.__load()


    def policies(self):
        return self.policies


    def __load(self):
        info("loading GPO from %s" % self.path)
        self.policies = []
        debug(self.path)
        gpt_path = "%s/%s" % (self.path, "GPT.INI")
        if not os.path.isfile(gpt_path):
            raise RuntimeError("%s not found" % gpt_path)

        gpt = SafeConfigParser()
        gpt.read(gpt_path)
        self.version = gpt['General']['Version']
        info("GPO version is %s" % self.version)
        files = (os.path.join(root,filename) for root, dirs, files in os.walk(self.path) for filename in files if fnmatch.fnmatch(filename, "*"))
        cse_pols = []
        for f in files:
            (cont, ent) = os.path.split(f)
            cont = cont[len(self.path):]
            info("found %s in %s" % (ent, cont))
            if ent.lower().endswith(".pol"):
                self.policies.append(self.__parse_pol(cont, ent))
            elif ent.lower() == "gpe.ini":
                p = "%s/%s/%s" % (self.path, cont, ent)
                info("parse GPO extensions in %s" % cont)
                self.gpe = GPE(self, p, self.path)
                cse_pols = [c['cse'] for c in self.gpe.cses]
        self.policies = list(chain.from_iterable(self.policies)) + cse_pols
        debug(self.policies)


    def __parse_pol(self, cont, ent):
        info("parse policy file %s in %s" % (ent, cont))
        path = "%s/%s/%s" % (self.path, cont, ent)
        res = []
        with open(path, 'rb') as f:
            signature = f.read(4)
            #if signature != b'\x67\x65\x52\x50':
            if signature != b'PReg':
                raise RuntimeError("%s is not valid .pol file" % path)

            version = f.read(4)
            if version != b'\x01\x00\x00\x00':
                raise RuntimeError("unsupported .pol file version")

            tmp = [ [ y[:-1].replace('\\', '/') for y in x[1:].split(';')] for x in f.read().decode('UTF-16').split(']') if x ]
            reg = [ dict(zip(['key', 'value', 'type', 'size', 'data'], x)) for x in tmp ]

        for p in reg:
            if p['key'] in polmap.keys():
                if p['value'] in polmap[p['key']]:
                    mod = importlib.import_module('gpom.pol.{}'.format(p['value'].lower()))
                    impl = mod.PolImpl(p)
                    res.append(impl)
                    print(impl.name)
                else:
                    error("unimplemented policy: %s/%s" % (p['key'], p['value']))
            else:
                error("unimplemented policy: %s" % p['key'])

        return res
