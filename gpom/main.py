import samba.param
from samba.credentials import Credentials
from samba.net import Net
from samba.dcerpc import nbt
from samba import smb
#import wbclient
import subprocess
import ldap, ldap.sasl
import os
import configparser
from functools import partial
from os.path import expanduser
import logging
import sys
import shutil
from datetime import datetime
from gpom.common import r2dn, dn_parent, parse_gplinks, parse_unc, config
from gpom.common import error, warning, info, debug
from gpom.user import User
from gpom.secdesc import SecurityDescriptor
from gpom.state import State
from gpom.gpo import GPO


class GPOM(object):
    __instance = None
    __initialized = False

    def __new__(cls):
        if GPOM.__instance is None:
            GPOM.__instance = object.__new__(cls)
        return GPOM.__instance


    def __init__(self):
        if not self.__initialized:
            self.gpo_cache_path = "%s/gpo" % config['GPO']['cache_dir']
            self.use_machine_creds = False

            self.__init_samba_params()
            self.__init_ldap()
            self.__init_state()
            self.__initialized = True


    def __init_state(self):
        self.state = State(config['Default']['db_path'], init=False)


    def __init_ldap(self):
        pdc = self.finddc()
        self.l = ldap.initialize('ldap://%s' % (pdc))
        self.l.procotol_version = 3
        self.l.set_option(ldap.OPT_X_SASL_NOCANON, True)
        auth_tokens = ldap.sasl.gssapi('')
        self.l.sasl_interactive_bind_s('', auth_tokens)
#        else:
#            self.l = ldap.initialize('ldaps://%s' % (pdc))
#            self.l.procotol_version = 3
#            self.l.set_option(ldap.OPT_X_SASL_NOCANON, True)
#            (name, domain) = self.creds.get_ntlm_username_domain()
#            password = self.creds.get_password()
#            debug('%s\n%s\n%s\n' % (name, domain, password))
#            self.l.simple_bind_s('%s@%s' % (name, domain), password)

        self.l.set_option(ldap.OPT_REFERRALS,0)


    def __init_samba_params(self, root_use_machine_creds = True):
        lp = samba.param.LoadParm()
        try:
            lp.load_default()
        except Exception as e:
            raise RuntimeError("cannot load default samba parameters", e)

        creds = Credentials()
        creds.guess(lp)
#        debug(os.getuid())
        if os.getuid() == 0 and root_use_machine_creds: # use machine credentials
            debug('use machine account')
#            creds.set_machine_account(lp)
            self.use_machine_creds = True

        self.lp = lp
        self.realm = lp.get('realm')
        self.base_dn = r2dn(self.realm)
        self.creds = creds
#        debug(creds.get_kerberos_state())


    def finddc(self, realm=None, flags=None):
        if not realm:
            realm = self.realm

        if not flags:
            flags = nbt.NBT_SERVER_LDAP | nbt.NBT_SERVER_DS | nbt.NBT_SERVER_WRITABLE

        net = Net(creds=self.creds, lp=self.lp)
        ret = net.finddc(domain=realm, flags=flags)
        return ret.pdc_dns_name


    def fetch(self, src, dst):
        [host, share, fname] = parse_unc(src)
        debug("UNC: %s" % ([host, share, fname]))
        conn = smb.SMB(str(host), share, lp=self.lp, creds=self.creds)
        dst_name = "%s/%s" % (dst, fname)
        debug("fetch %s from %s to %s" % (fname, host, dst_name))
        data = conn.loadfile(fname)
        open(dst_name, 'w').write(data)


    def fetch_dir(self, unc, dst, recursive=True):
        [dom_name, service, src] = parse_unc(unc)
        debug("UNC: %s" % ([dom_name, service, src]))
        conn = smb.SMB(self.finddc(realm=dom_name), service, lp=self.lp, creds=self.creds)

        if not os.path.isdir(dst):
            os.mkdir(dst)

        r_dirs = [ src ]
        l_dirs = [ dst ]
        attr_flags = smb.FILE_ATTRIBUTE_SYSTEM | \
                     smb.FILE_ATTRIBUTE_DIRECTORY | \
                     smb.FILE_ATTRIBUTE_ARCHIVE | \
                     smb.FILE_ATTRIBUTE_HIDDEN

        while r_dirs:
            r_dir = r_dirs.pop()
            l_dir = l_dirs.pop()
            dirlist = conn.list(r_dir, attribs=attr_flags)
            for e in dirlist:
                r_name = "%s\\%s" % (r_dir, e['name'])
                l_name = os.path.join(l_dir, e['name'])

                if e['attrib'] & smb.FILE_ATTRIBUTE_DIRECTORY:
                    r_dirs.append(r_name)
                    l_dirs.append(l_name)
                    os.mkdir(l_name)
                else:
                    data = conn.loadfile(r_name)
                    open(l_name, 'w').write(data)



    def find_user(self, name):
        expr = '(&(|(samAccountName=%s)(samAccountName=%s$))(objectClass=User))' % (name, name)
        res = self.search(expr=expr)
        if not res:
            return None

        (user_dn, _) = res[0]
#        (_, res) = self.search(dn=user_dn, scope=ldap.SCOPE_BASE, attrs=['objectClass'])[0]
        (_, res) = self.search(dn=user_dn, scope=ldap.SCOPE_BASE, attrs=[])[0]
        is_computer = 'computer' in res['objectClass']

        user = User(dn=user_dn, is_computer=is_computer)
        res = subprocess.check_output(["wbinfo", "-n", "'%s'" % name])
        user.sid = res.split(' ',1)[0]
        debug(user.sid)
        res = subprocess.check_output(["wbinfo", "--user-sids=%s" % user.sid])
        user.groups = [ s for s in res.split('\n') if s and s != user.sid ]
        debug(user.groups)

        return user


    def find_gplinks(self, name):
        user = self.find_user(name)
        dn = dn_parent(user.dn)
        # FIXME:
        dn = dn_parent(dn)
        debug("DN: %s" % dn)
        (_, res) = self.search(dn=dn, scope=ldap.SCOPE_BASE, attrs=['gPLink', 'gPOptions'])[0]
        debug("RES: %s" % res)
        gplinks = []
        if res:
            gplinks = parse_gplinks(res['gPLink'])

        return gplinks


#    def gpo_list(self):
#        conts = '<WKGUID=%s,%s>' % ('AB1D30F3768811D1ADED00C04FD8D5CD', r2dn(self.realm)) #self.def_conts('system')
#        expr = '(objectClass=groupPolicyContainer)'
#        res = self.search(dn=conts, scope=ldap.SCOPE_SUBTREE, expr=expr, attrs=['displayName'])
#        return res


    def default_domain_policy(self):
        dn = 'CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,%s' % (r2dn(self.realm))
        (_, res) = self.search(dn=dn, scope=ldap.SCOPE_BASE, attrs=['name', 'displayName', 'flags', 'gPCFileSysPath', 'whenChanged', 'nTSecurityDescriptor'])[0]
        sd = self.get_ntsecdesc(dn)
        res['nTSecurityDescriptor'] = sd
        return res


    def default_domain_controllers_policy(self):
        dn = 'CN={6AC1786C-016F-11D2-945F-00C04FB984F9},CN=Policies,CN=System,%s' % (r2dn(self.realm))
        (dn, res) = self.search(dn=dn, scope=ldap.SCOPE_BASE, attrs=['name', 'displayName', 'flags', 'gPCFileSysPath', 'whenChanged'])[0]
        sd = self.get_ntsecdesc(dn)
        res['nTSecurityDescriptor'] = sd

        return res


    def find_gpo(self, name, apply_perms=False):
        gplinks = self.find_gplinks(name)
#        debug("FIND_GPO (main)")

#        if not gplinks:
#            return []

        user = self.find_user(name)
        gpos = []
        for link in gplinks:
            debug(link['dn'])
            (dn, res) = self.search(dn=link['dn'], scope=ldap.SCOPE_BASE, attrs=['name', 'displayName', 'flags', 'gPCFileSysPath', 'whenChanged', 'nTSecurityDescriptor'])[0]
            sd = self.get_ntsecdesc(dn)
            res['nTSecurityDescriptor'] = sd
#            debug(res)
            secdesc = SecurityDescriptor(sd)
#            debug(secdesc)
            if apply_perms and not secdesc.is_gpo_apply_allowed([user.sid] + user.groups):
                continue
            gpos.append(res)

        ddp = self.default_domain_policy()
        secdesc = SecurityDescriptor(ddp['nTSecurityDescriptor'])
        if not apply_perms:
            gpos.append(ddp)
        elif secdesc.is_gpo_apply_allowed([user.sid] + user.groups):
            gpos.append(ddp)

        return gpos


    def get_gpo(self, name, apply_perms=True, force=False):
        gpos_ldap = self.find_gpo(name, apply_perms)
        gpos = []

        for g in gpos_ldap:
            self.fetch_gpo(g, force)
            gpo = GPO(path='%s/%s' % (self.gpo_cache_path, g['name'][0]), name=g['displayName'][0], whenChanged=g['whenChanged'][0])
            payloads = []
            for pol in gpo.policies:
                if pol.payload:
                    payloads += pol.payload
            gpos.append(gpo)

        self.gpos = gpos
#        debug("SELF GPO: %s" % self.gpos)
        return self.gpos


    def fetch_gpo(self, gpo, force=False):
        gpo_name = gpo['displayName'][0]
        gpo_whenChanged = gpo['whenChanged'][0]
        l_time = self.state.get(gpo_name, 'whenChanged')
#        gpo_guid = gpo['name'][0]
        gpo_path = "%s/%s" % (self.gpo_cache_path, gpo['name'][0])
#        gpo_path = gpo['path']
        gpo_link_path = "%s/%s" % (self.gpo_cache_path, gpo_name)

        if l_time:
            l_time = datetime.strptime(l_time, '%Y%m%d%H%M%S.%fZ')

        try:
            r_time = datetime.strptime(gpo_whenChanged, '%Y%m%d%H%M%S.%fZ')
        except Exception as e:
            raise ValueError("Got invalid datetime format from remote. Expected '%Y%m%d%H%M%S.%fZ' but got %s" % gpo_whenChanged)

        debug('remote time for %s is %s' % (gpo_name, r_time))
        debug('local time for %s is %s' % (gpo_name, l_time))

        if not force and l_time and l_time >= r_time:
            debug("local time match remote time. No need to update")
            return

        l_dir = gpo_path
        if os.path.isdir(l_dir):
            link_name = "%s/%s" % (self.gpo_cache_path, gpo_name)
            if os.path.exists(link_name):
                os.unlink(link_name)
            shutil.rmtree(l_dir)

        os.makedirs(l_dir)
        os.symlink(l_dir, "%s/%s" % (self.gpo_cache_path, gpo_name))

        for unc in gpo['gPCFileSysPath']:
            self.fetch_dir(unc, l_dir, recursive=True)
        self.state.set(gpo_name, 'whenChanged', gpo_whenChanged)


    def update_policy_payload(self, pol):
        if not os.path.isdir(pol.cache_path):
            os.makedirs(pol.cache_path)

        for p in pol.payload if pol.payload else []:
            target_path = "%s/%s" % (pol.cache_path, p.rsplit('/',1)[0])
            if not os.path.isdir(target_path):
                os.makedirs(target_path)
            debug("update payload %s" % p)
            self.fetch(p, target_path)


    def get_ntsecdesc(self, dn):
        sd_flags = ldap.controls.RequestControl(controlType='1.2.840.113556.1.4.801',
                                                criticality=True,
                                                encodedControlValue=b'\x30\x03\x02\x01\x04')
        try:
            res = self.l.search_ext_s(dn,
                                      ldap.SCOPE_SUBTREE,
                                      filterstr='(objectClass=*)',
                                      attrlist=['nTSecurityDescriptor'],
                                      attrsonly=True,
                                      serverctrls=[sd_flags])
        except Exception as e:
            print("search %s failed with %s" % (dn, e))
            raise

        (_, r) = res[0]
        return r['nTSecurityDescriptor'][0]


    def search(self, dn=None, expr=None, scope=ldap.SCOPE_SUBTREE, attrs=[]):
        if not dn:
            dn = self.base_dn

        try:
            if not expr:
                expr = '(objectClass=*)' # fix for old ldap (should accept None)

            res = self.l.search_s(dn, scope, expr, attrs)
        except Exception as e:
            print("search %s on %s failed with %s" % (expr, dn, e))
            raise

        ret = [ (r, dn) for (r, dn) in res if r ]
        return ret if ret else None


    def apply(self, acc):
        gpos = self.get_gpo(acc)
        for g in gpos:
            debug(g.path)
            debug("policies: %s" % g.policies)
            for p in g.policies:
                debug("update payload")
                self.update_policy_payload(p)
                debug("apply policy")
                p.apply()
