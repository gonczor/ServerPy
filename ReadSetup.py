import re

__config_file_name__ = 'PyHomeServer.conf'
__port_pattern__ = 'Port: ([0-9]+)'
__address_pattern__ = 'Address: ([0-9]+.[0-9]+.[0-9]+.[0-9]+)+'


def get_setup():
    """Return setup in form of address, port"""
    contents = __get_file_contents__()
    address = __get_address__(contents)
    port = __get_port__(contents)
    return address, port


def __get_file_contents__():
    f = open(__config_file_name__, 'r')
    contents = f.read()
    f.close()
    return contents


def __get_port__(content):
    port = re.search(__port_pattern__, content)
    return int(port.group(1))


def __get_address__(content):
    address = re.search(__address_pattern__, content)
    return address.group(1)
