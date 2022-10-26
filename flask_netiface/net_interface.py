import psutil
import subprocess
import re


def get_interfaces_info():
    interfaces = {}
    addrs = psutil.net_if_addrs()
    for interface in addrs:
        cmd = f'ip link show {interface}'.split()
        state_flags = re.findall(b'<.*>', subprocess.check_output(cmd))[0]
        state = 'UP' if 'UP' in state_flags.decode('utf-8') else 'DOWN'
        interfaces[interface] = {
                'state': state,
                'ipv4': [],
                'ipv4_mask': [],
                'ipv6': [],
                'ipv6_mask': [],
                'MAC': ''}
        for snicaddr in addrs[interface]:
            name = snicaddr.family.name
            address = snicaddr.address
            if '%' in address:
                address = address[0:address.find('%')]
            mask = snicaddr.netmask
            if name == 'AF_INET':
                interfaces[interface]['ipv4'].append(address)
                interfaces[interface]['ipv4_mask'].append(mask)
            elif name == 'AF_INET6':
                interfaces[interface]['ipv6'].append(address)
                interfaces[interface]['ipv6_mask'].append(mask)
            elif snicaddr.family.name == 'AF_PACKET':
                interfaces[interface]['MAC'] = address

    return interfaces
