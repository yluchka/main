from IPy import IP


def convert_to_bin(ip: str) -> str:
    """
    ancillary function
    convert ip-address from decimal to binary form
    >>> convert_to_bin('192.168.1.1')
    '11000000.10101000.00000001.00000001'
    """
    ip = '.'.join([bin(int(i) + 256)[3:] for i in ip.split('.')])
    return ip


def mask(raw_address: str) -> list:
    """
    ancillary function
    returns the mask items in the list
    >>> mask('91.124.230.205/30')
    [255, 255, 255, 252]
    """
    prefix = int(raw_address[(raw_address.find('/')) + 1:])
    mask = [0, 0, 0, 0]
    for i in range(prefix):
        mask[i // 8] += 1 << (7 - i % 8)
    return mask


def broadcast(raw_address: str) -> str:
    """
    ancillary function
    returns broadcast address from raw address
    >>> broadcast('91.124.230.205/30')
    '91.124.230.207'
    """
    ip_address = get_ip_from_raw_address(raw_address).split('.')
    mask_address = mask(raw_address)
    broadcast_address = []
    j = 0
    for i in mask_address:
        a = int(ip_address[j]) | (255 - int(i))
        broadcast_address.append(str(a))
        j += 1
    broadcast_address = '.'.join(broadcast_address)
    return broadcast_address


def get_ip_from_raw_address(raw_address: str) -> str:
    """
    returns ip-address from raw_address
    >>> get_ip_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    return raw_address[:(raw_address.find('/'))]


def get_network_address_from_raw_address(raw_address: str) -> str:
    """
    finds network address from raw address
    >>> get_network_address_from_raw_address('192.168.1.15/24')
    '192.168.1.0'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    ip_address = get_ip_from_raw_address(raw_address).split('.')
    mask_address = mask(raw_address)
    network_address = []
    for i in range(4):
        a = int(ip_address[i]) & mask_address[i]
        network_address.append(str(a))
    network_address = '.'.join(network_address)
    return network_address


def get_binary_network_address_from_raw_address(raw_address: str) -> str:
    """
    returns binary network address from raw address
    >>> get_binary_network_address_from_raw_address('192.168.1.15/24')
    '11000000.10101000.00000001.00000000'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    network_address = get_network_address_from_raw_address(raw_address)
    bin_network_address = convert_to_bin(network_address)
    return bin_network_address


def get_mask_from_raw_address(raw_address: str) -> str:
    """
    returns mask from raw address
    >>> get_mask_from_raw_address('91.124.230.205/30')
    '255.255.255.252'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    mask_address = mask(raw_address)
    new_mask_address = [str(i) for i in mask_address]
    new_mask_address = '.'.join(new_mask_address)
    return new_mask_address


def get_second_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    returns the second possible node address on the given network
    >>> get_second_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.206'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    net = get_network_address_from_raw_address(raw_address)
    x = int(net[net.rfind('.') + 1:]) + 2
    second = net[:net.rfind('.') + 1] + str(x)
    return second


def get_last_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    returns the last possible node address on the given network
    >>> get_last_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.206'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    broad = broadcast(raw_address)
    x = int(broad[broad.rfind('.') + 1:]) - 1
    last = broad[:broad.rfind('.') + 1] + str(x)
    return last


def get_total_number_of_ips_from_raw_address(raw_address: str) -> int:
    """
    retruns total number of ips
    >>> get_total_number_of_ips_from_raw_address('91.124.230.205/30')
    4
    >>> get_total_number_of_ips_from_raw_address('172.20.0.0/14')
    262144
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    index_mask = raw_address[raw_address.rfind('/') + 1:]
    numbers = 2 ** (32 - int(index_mask))
    return numbers


def get_ip_class_from_raw_address(raw_address: str) -> str:
    """
    returns the name of network class
    >>> get_ip_class_from_raw_address('91.124.230.205/30')
    'A'
    >>> get_ip_class_from_raw_address('191.124.230.205/30')
    'B'
    >>> get_ip_class_from_raw_address('212.124.230.205/30')
    'C'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    ip_start = int(raw_address[:raw_address.find('.')])
    if ip_start <= 127:
        return 'A'
    elif ip_start <= 191:
        return 'B'
    elif ip_start <= 223:
        return "C"


def get_ip_address_type_from_raw_address(raw_address: str) -> str:
    """
    returns type IP-address: "Private" or "Public"
    >>> get_ip_address_type_from_raw_address('172.23.230.205/30')
    'Private'
    >>> get_ip_address_type_from_raw_address('72.23.230.205/30')
    'Public'
    """
    try:
        IP(raw_address[:(raw_address.find('/'))])
    except:
        return None
    pub = "Public"
    priv = "Private"
    if raw_address.startswith('10.') or raw_address.startswith('192.168.'):
        return priv
    elif raw_address.startswith('172.'):
        a = int(raw_address.split(".")[1])
        if a in range(16, 32):
            return priv
    else:
        return pub


def user_and_checks_function():
    """
    accepts the ip-address, verifies that the correct
    user input, returns the necessary data
    """
    raw_address = input("Ip-address and mask: ")
    try:
        IP(get_ip_from_raw_address(raw_address))
    except:
        return 'Error'
    try:
        prefix = int(raw_address[(raw_address.find('/') + 1):])
        if prefix in range(0, 33):
            pass
        else:
            return 'Missing prefix'
    except ValueError:
        return 'Missing prefix'

    print(f"IP address: {get_ip_from_raw_address(raw_address)}")
    print(f"Network Address: {get_network_address_from_raw_address(raw_address)}")
    print(f"Binary Network Address: {get_binary_network_address_from_raw_address(raw_address)}")
    print(f"Subnet Mask: {get_mask_from_raw_address(raw_address)}")
    print(f"Second usable host IP: {get_second_usable_ip_address_from_raw_address(raw_address)}")
    print(f"Last usable host IP: {get_last_usable_ip_address_from_raw_address(raw_address)}")
    print(f"Total number of IP addresses: {get_total_number_of_ips_from_raw_address(raw_address)}")
    print(f"IP class: {get_ip_class_from_raw_address(raw_address)}")
    print(f"IP type: {get_ip_address_type_from_raw_address(raw_address)}")
    return ""


if __name__ == "__main__":
    print(user_and_checks_function())
    import doctest

    print(doctest.testmod())
