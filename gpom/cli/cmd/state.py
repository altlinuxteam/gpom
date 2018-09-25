import argparse
from gpom.cli import Command
from gpom.common import config, error, warning, info, debug #, SambaParams
from gpom.state import state


class CMDImpl(Command):
    def __init__(self):
        super(CMDImpl, self).__init__()
        self.cmd = 'state'
        self.help = 'Manage local policy state'
        self.gpos = None

    def init_subparser(self, sub):
        p = sub.add_parser(self.cmd, help=self.help)
        s = p.add_subparsers(dest="command", help="%s commands" % self.cmd)
        self.subcommands(s)
        self.parser = p

    def subcommands(self, sub):
        show = sub.add_parser("show", help="show current status")
        show.add_argument("--json", help="output in JSON format", action="store_true")

        init = sub.add_parser("init", help="create empry state directory")
        init.add_argument("--force", help="force overwrite existing data", default=False, action="store_true")

    def __run__(self, args):
        print(args)
        if args.command == "init":
            self.gpos = state.__init__(init=True, force=args.force)
        elif not self.gpos:
            self.gpos = state

        debug("executing %s command" % args.command, self)
        print(self.gpos.state)
