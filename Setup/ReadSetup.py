import re

_config_file_name = 'Configuration/PyHomeServer.conf'
_port_pattern = 'Port: ([0-9]+)'
_address_pattern = 'Address: ([0-9]+.[0-9]+.[0-9]+.[0-9]+)+'


def get_setup():
    """Return setup in form of address, port"""
    contents = _get_file_contents()
    address = _get_address(contents)
    port = _get_port(contents)
    return address, port


def _get_file_contents():
    f = open(_config_file_name, 'r')
    contents = f.read()
    f.close()
    return contents


def _get_port(content):
    port = re.search(_port_pattern, content)
    return int(port.group(1))


def _get_address(content):
    address = re.search(_address_pattern, content)
    return address.group(1)
