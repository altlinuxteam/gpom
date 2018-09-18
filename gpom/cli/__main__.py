import argparse
import sys
import importlib
from gpom.common import config, error, warning, info, debug #, SambaParams

def main():
    rootp = argparse.ArgumentParser()
    creds = rootp.add_mutually_exclusive_group(required=False)
    creds.add_argument('--creds', help='username:password', action='store')
    creds.add_argument('--kerberos', help='use kerberos', action='store_true')
    sub = rootp.add_subparsers(help='commands', dest='cmd')
    sub.required = True

    #cmd_list = ['state', 'gpo']
    #cmd_list = ['gpo', 'state']
    cmd_list = ['policy']
    commands = {}

    debug("import CLI commands")
    for c in cmd_list:
        debug(c)
        try:
            mod = importlib.import_module("gpom.cli.cmd.%s" % c)
            impl = mod.CMDImpl()
        except Exception as e:
            raise RuntimeError("Cannot load module for %s: %s" % (c, e))

        debug("add '%s' to the commands list" % impl.cmd)
        impl.init_subparser(sub)
        commands[impl.cmd] = impl

    args = rootp.parse_args()
    commands[args.cmd].run(args)

if __name__ == "__main__":
    main()
