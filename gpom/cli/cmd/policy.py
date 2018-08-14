import argparse
from gpom.cli import Command
from gpom.common import config, error, warning, info, debug #, SambaParams
from gpom.main import GPOM
import os


class CMDImpl(Command):
    def __init__(self):
        super(CMDImpl, self).__init__()
        self.cmd = 'policy'
        self.help = 'Policy Management'
        self.gpom = GPOM()

    def init_subparser(self, sub):
        p = sub.add_parser(self.cmd, help=self.help)
        s = p.add_subparsers(dest="command", help="%s commands" % self.cmd)
        self.subcommands(s)
        self.parser = p


    def subcommands(self, sub):
#        show = sub.add_parser("apply", help="list GPO containers")
#        show.add_argument("account", help="account name")

        apply = sub.add_parser("apply", help="apply policy")
        apply.add_argument("account", help="account name", nargs='*', default=None)
        apply.add_argument("--host", help="use current hostname as an account name", action='store_true')

#        showpols = sub.add_parser("showpols", help="show policies list of GPO")
#        showpols.add_argument("guid", help="GPO GUID")


    def __run__(self, args):
        if args.command == "apply":
            if args.host:
                debug('use hostname as an account name')
                args.account = '%s$' % os.getenv('HOSTNAME').split('.',1)[0]

            debug('apply policies for %s' % args.account)
            self.gpom.apply(args.account)
