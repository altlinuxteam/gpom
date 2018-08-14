import logging
import sys
import configparser
from functools import partial
from os.path import expanduser


def r2dn(r):
    return ','.join(['DC=%s' % x for x in r.lower().split('.')])


def parse_unc(unc):
    if unc.startswith('\\\\'):
        return unc[2:].split('\\',2)
    elif unc.startswith('//'):
        return unc[2:].split('/', 2)
    else:
        raise ValueError("UNC %s doesn't start with \\\\ or //" % unc)


def stringify_ldap(data):
    if type(data) == dict:
        for key, value in data.items():
            data[key] = stringify_ldap(value)
        return data
    elif type(data) == list:
        new_list = []
        for item in data:
            new_list.append(stringify_ldap(item))
        return new_list
    elif type(data) == tuple:
        new_tuple = []
        for item in data:
            new_tuple.append(stringify_ldap(item))
        return tuple(new_tuple)
    elif PY2 and type(data) == unicode:
        return str(data)
    elif PY3 and type(data) == bytes:
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return data
    else:
        return data


def dn_parent(dn):
    return dn.split(',',1)[1]


def parse_gplinks(gpls):
    res = []
    gps = [ x[1:] for x in gpls[0].split(']') if x ]
    for gpl in gps:
        [a, b] = gpl.split(';')
        c = {'dn': a[7:],
             'opts': int(b)
            }
        res.append(c)
    return res


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def format_msg(msg, obj):
    if obj:
        str = "[MODULE: %s] %s" % (repr(obj), msg)
    else:
        str = "%s" % msg

    return str

def debug(msg, obj = None):
    logging.debug(format_msg(msg, obj))

def info(msg, obj = None):
    logging.info(format_msg(msg, obj))

def warning(msg, obj = None):
    logging.warning(format_msg(msg, obj))

def error(msg, obj = None):
    logging.error(format_msg(msg, obj))


config = configparser.SafeConfigParser(
    {'db_path': '/var/lib/gpom/state'
    }
)

config.add_section('GPOS')
c = partial(config.set, 'GPOS')
c('db_path', '/var/lib/gpom/state')

config.read("/etc/gpom.conf")
config.read("%s/.config/gpom/gpom.conf" % expanduser("~"))
config.read("./gpom.conf")
