from gpom.common import config, error, warning, info, debug
import os


class Policy(object):
    def __init__(self):
        self.payload = None
        self.cache_path = config['Policy']['cache_dir']


    def apply(self):
        if not hasattr(self, '__apply__'):
            error("apply procedure is unimplemented for policy %s" % self.name)
            return

#        if hasattr(self, 'payload') and self.payload:
#            self.update_payload()

        self.__apply__()


    def get_local_state(self):
        raise RuntimeError("get_local_state function is undefined in %s policy" % self.name)


    def pol2state(self):
        raise RuntimeError("pol2state function is undefined in %s policy" % self.name)


    def __compare__(self):
        raise RuntimeError("__compare__ function is undefined in %s policy" % self.name)


    def state_diff(self):
        local_state = self.get_local_state()
        policy_state = self.pol2state()
        return self.__compare__(local_state, policy_state)

#    def prefetch(self):
#        if hasattr(self, 'payload') and self.payload:
#            debug("fetching payload for policy %s form %s" % (self.name, self.payload))



class DesktopPolicy(Policy):
    def __init__(self):
        super(DesktopPolicy, self).__init__()
        self.target = 'desktop'
        self.scope = Scope('user')



class Scope:
    def __init__(self, scope):
        if scope not in ['user', 'machine']:
            raise ValueError("%s is not valid scope name" % scope)

        self.name = scope
