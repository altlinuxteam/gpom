class User(object):
    def __init__(self, dn=None, is_computer=False, sid=None, groups=None):
        self.dn = dn
        self.is_computer = is_computer
        self.sid = sid
