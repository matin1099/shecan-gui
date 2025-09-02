import subprocess
import ctypes
import sys
import os

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the script with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()


def shecan(custom_dns, custom_alt_dns, adapter="Ethernet"):
    adapter_name = adapter
    preferred_dns = custom_dns
    alternate_dns = custom_alt_dns

    def run_cmd(cmd):
        #print(f"> {' '.join(cmd)}")
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(cmd,
                                capture_output=False,#True,
                                text=False,#True,
                                shell=False,
                                startupinfo=si,
                                creationflags=subprocess.CREATE_NO_WINDOW)#True)
        # if result.stdout:
        #     print(result.stdout.strip())
        # if result.stderr:
        #     print(result.stderr.strip())

    run_cmd(["netsh", "interface", "ip", "set", "dns",
             f'name={adapter_name}', "static", preferred_dns, "primary"])
    run_cmd(["netsh", "interface", "ip", "add", "dns",
             f'name={adapter_name}', alternate_dns, "index=2"])


def clean_shecan(adapter="Ethernet"):
    adapter_name = adapter

    def run_cmd(cmd):
        #print(f"> {' '.join(cmd)}")
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(cmd,
                                capture_output=False,#True,
                                text=False,#True,
                                shell=False,
                                startupinfo=si,
                                creationflags=subprocess.CREATE_NO_WINDOW)#True)
        # if result.stdout:
        #     print(result.stdout.strip())
        # if result.stderr:
        #     print(result.stderr.strip())

    # Reset DNS to automatic for IPv4
    run_cmd(["netsh", "interface", "ip", "set", "dns", f'name={adapter_name}', "dhcp"])

    # Optional: also reset IPv6 DNS to automatic
    run_cmd(["netsh", "interface", "ipv6", "set", "dnsservers", f'name={adapter_name}', "dhcp"])
