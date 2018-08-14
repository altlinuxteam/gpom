from samba.ndr import ndr_unpack, ndr_print
from samba.dcerpc import security
from maps.car import CAR
from common import error, warning, info, debug


class SecurityDescriptor(object):
    def __init__(self, secdesc):
        self.secdesc = ndr_unpack(security.descriptor, secdesc)
        self.sddl = self.secdesc.as_sddl()


    def is_gpo_apply_allowed(self, sids):
        car = CAR()
        apply_gpo_guid = car.byname('Apply-Group-Policy')
        sids = map(lambda x: str(x), sids)
        for a in self.secdesc.dacl.aces:
            if (a.type == 6 and str(a.object.type) == apply_gpo_guid) and str(a.trustee) in sids:
                return False

        return True
