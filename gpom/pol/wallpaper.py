from gpom.common import config, error, warning, info, debug
from gpom.policy import DesktopPolicy
#from gpom.common import SmbClient
import subprocess
import re
import os


def _escape_single_quotes(string):
    return re.sub("'", r"'\''", string)

class PolImpl(DesktopPolicy):
    def __init__(self, reg):
        super(PolImpl, self).__init__()
        self.name = 'Wallpaper'
        self.payload = [reg['data']]


    def desktop_name(self):
        de = None
        if 'XDG_CURRENT_DESKTOP' in os.environ.keys():
            de = os.environ['XDG_CURRENT_DESKTOP']
        return de

    def __apply__(self):
        de = self.desktop_name()
        if not de:
            error("Cannot determine DE")
            debug("Set policy state as NOT IMPLEMENTED")
            return
        if de == 'MATE':
            debug("Looks like DE is MATE")
            key = "/org/mate/desktop/background/picture-filename"
            value = "%s/%s" % (config['Policy']['cache_dir'], self.payload[0])
            command = " ".join([
#                'export `/usr/bin/dbus-launch`',
#                ';',
                '/usr/bin/dconf write', key, "\"'%s'\"" % _escape_single_quotes(value),
#                ';',
#                'kill $DBUS_SESSION_BUS_PID &> /dev/null'
            ])
#            command = '/usr/bin/dconf write %s %s' % (key, "\"'%s'\"" % _escape_single_quotes(value))

            debug(command)
            res = subprocess.check_output(['/bin/sh', '-c', command]).strip()
            debug("result: %s" % res)
