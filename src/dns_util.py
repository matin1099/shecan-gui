import subprocess

def get_dns_servers( ):
    try:
        # Run the netsh command to get DNS info
        output = subprocess.check_output(["netsh", "interface", "ip", "show", "dns"], encoding="utf-8")
    except subprocess.CalledProcessError as e:
        print("Failed to query DNS settings.")
        return set()

    dns_servers = set()

    for line in output.splitlines():
        line = line.strip()
        if (line.startswith("Statically Configured DNS Servers") or
                line.startswith("DNS Servers configured through DHCP")):
            # The next lines contain the DNS IPs
            continue
        if line and "." in line:
            dns_servers.add(line.strip())

    return dns_servers


def check_dns():
    is_VPN = False
    is_shecanPrivate1 = False
    is_shecanPrivate2 = False
    is_noDNS = False

    current_dns = get_dns_servers()
    # print("Current DNS servers: ", current_dns)
    for item in current_dns:
        if '172.19.100.11' in item:
            is_noDNS = True

        if '78.22.122.101' in item:
            is_shecanPrivate1 = True

        if '185.51.200.1' in item:
            is_shecanPrivate2 = True

        if '1.1.1.1' in item:
            is_VPN = True

    if is_noDNS and not (is_shecanPrivate1 or is_shecanPrivate2 or is_VPN):
        return ('no DNS')
    elif is_shecanPrivate1 or is_shecanPrivate2:
        return ('private shecan')
    elif is_VPN:
        return ('VPN')
