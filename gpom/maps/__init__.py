class GUIDMAP(object):
    def byguid(self, guid):
        m = dict((g,t) for t,g in self.m)
        return m.get(guid, None)


    def byname(self, name):
        m = dict((t,g) for t,g in self.m)
        return m.get(name, None)


    def get_mapping(self):
        return self.m
