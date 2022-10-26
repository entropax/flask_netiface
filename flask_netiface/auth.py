import subprocess


def sudo_perm_validator(password):
    password = bytes(password, encoding='utf-8')
    subprocess.run(['sudo', '-kK'])
    cmd = ['sudo -S echo test']
    result = subprocess.run(
            cmd,
            shell=True,
            input=password)
    if result.returncode != 0:
        return False
    return True
