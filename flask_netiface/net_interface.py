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


def switch_interface_status(interface, status, password):
    password = bytes(password, encoding='utf-8')
    if status == 'UP':
        cmd = f'sudo -S ip link set dev {interface} down'.split()
        subprocess.run(
            cmd,
            shell=False,
            input=password,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    else:
        cmd = f'sudo -S ip link set dev {interface} up'.split()
        subprocess.run(
            cmd,
            shell=False,
            input=password,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)


def add_ip_address(interface, address, password):
    password = bytes(password, encoding='utf-8')
    cmd = f'sudo -S ip a add {address} dev {interface}'.split()
    subprocess.run(
            cmd,
            shell=False,
            input=password,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)


def delete_ip_address(interface, address, password):
    password = bytes(password, encoding='utf-8')
    cmd = f'sudo -S ip a del {address} dev {interface}'.split()
    subprocess.run(
            cmd,
            shell=False,
            input=password,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)


def change_ip_address(interface, new_ip, old_ip, password):
    add_ip_address(interface, new_ip, password)
    delete_ip_address(interface, old_ip, password)


def change_ip_mask(interface, ip_address, new_mask, password):
    password = bytes(password, encoding='utf-8')
    delete = f'sudo -S ip a del {ip_address} dev {interface}'.split()
    add = f'sudo -S ip a add {ip_address}/{new_mask} dev {interface}'.split()
    subprocess.run(
            delete,
            shell=False,
            input=password,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    subprocess.run(
            add,
            shell=False,
            input=password,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
