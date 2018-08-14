from gpom.common import config, error, warning, info, debug
from gpom.policy import Policy
import importlib
import os


def load(gpo, cse, is_machine_policy):
    try:
        mod = importlib.import_module('gpom.cses.%s' % cse)
        impl = mod.CSEImpl(gpo, is_machine_policy)
    except Exception as e:
        raise NotImplementedError('CSE module for %s not found. %s' % (cse,e))

    return impl


class CSE(Policy):
    def __init__(self):
        super(CSE, self).__init__()
#        raise NotImplementedError('do not use this class directly!')


    def parse(self, gpo_path):
        for (pf, parser) in self.pref_files:
            prefix = 'Machine' if self.is_machine_policy else 'User'
            path = "%s/%s/%s" % (gpo_path, prefix, pf)
            if not os.path.isfile(path):
                raise RuntimeError("%s not found" % path)

            parser(path)
