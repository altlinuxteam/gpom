import argparse
from cli import Command
from gpom.common import config, error, warning, info, debug #, SambaParams
#from gpom.gpor import GPOR
#from gpom.gpos import state
#from gpom.common import SambaParams

class CMDImpl(Command):
    def __init__(self):
        super(CMDImpl, self).__init__()
        self.cmd = 'gpo'
        self.help = 'Group Policy Object'
        self.gpor = None
        self.gpos = None
#        self.sp = SambaParams()

    def init_subparser(self, sub):
        p = sub.add_parser(self.cmd, help=self.help)
        s = p.add_subparsers(dest="command", help="%s commands" % self.cmd)
        self.subcommands(s)
        self.parser = p


    def subcommands(self, sub):
        show = sub.add_parser("list", help="list GPO containers")
        show.add_argument("account", help="account name")

        fetch = sub.add_parser("fetch", help="fetch GPOs for account")
        fetch.add_argument("account", help="account name")
        fetch.add_argument("--force", help="force update", action='store_true')

        showpols = sub.add_parser("showpols", help="show policies list of GPO")
        showpols.add_argument("guid", help="GPO GUID")

        apply = sub.add_parser("apply", help="apply all policies from GPO")
        apply.add_argument("guid", help="GPO GUID")


    def __run__(self, args):
        if not self.gpos:
            self.gpos = state

        if not self.gpor:
            self.gpor = GPOR(self.sp.lp, self.sp.creds, self.gpos)

        if args.command == "list":
            gpcs = self.gpor.list(args.account)
            if not gpcs:
                print("no GPOs found for %s" % args.account)
                return

            for gpc in gpcs:
                print("%-16s %s" % (gpc['displayName'][0], gpc['name'][0]))

        elif args.command == "fetch":
            gpcs = self.gpor.list(args.account)
            self.gpor.fetch(gpcs, force=args.force)

        elif args.command == "showpols":
            if not args.guid.startswith('{'):
                guid = "{%s}" % args.guid
            else:
                guid = args.guid

            policies = self.gpor.gpo_policies(guid)
            if not policies:
                print("No policies in %s" % guid)
                return

            for p in policies:
                print(p.name, p.payload)

        elif args.command == "apply":
            if not args.guid.startswith('{'):
                guid = "{%s}" % args.guid
            else:
                guid = args.guid

#            policies = self.gpor.gpo_policies(guid)
            gpo = self.gpor.get_gpo(guid)

            if not gpo.policies:
                print("No policies in %s" % guid)
                return

            for p in gpo.policies:
                p.apply()

            debug("apply CSEs")
            for c in gpo.gpe.cses:
                print(c)
                st = c['cse'].get_local_state()
