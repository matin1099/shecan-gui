from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QMainWindow, QLabel, QPushButton,)
import subprocess

# main window structure
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #reading DNS
        self.status = self.check_dns()


        self.setWindowTitle('Shecan')

        # first container
        # Contain two line two column
        # left column label
        # right column GETTED DNS

        #First Row

        self.dns = QLabel()
        self.dns.setText("DNS:")
        self.dns_get = QLabel()


        self.alt_dns = QLabel()
        self.alt_dns.setText("Alternative DNS:")
        self.alt_dns_get = QLabel()


        first_row_container = QHBoxLayout()
        first_row_container.addWidget(self.dns)
        first_row_container.addWidget(self.dns_get)


        second_row_container = QHBoxLayout()
        second_row_container.addWidget(self.alt_dns)
        second_row_container.addWidget(self.alt_dns_get)

        box_layout = QVBoxLayout()
        box_layout.addLayout(first_row_container)
        box_layout.addLayout(second_row_container)

        #setting GET_LABELs text
        self.dns_get.setText(self.status)
        self.alt_dns_get.setText(self.status)

        whole_container = QWidget()
        whole_container.setLayout(box_layout)
        self.setCentralWidget(whole_container)  # ← THIS is important

    def get_dns_servers(self,):
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

    def check_dns(self):
        is_VPN = False
        is_shecanPrivate1 = False
        is_shecanPrivate2 = False
        is_noDNS = False

        current_dns = self.get_dns_servers()
        for item in current_dns:
            if '172.19.100.11' in item:
                is_noDNS = True

            if  '78.22.122.101'in item:
                is_shecanPrivate1 = True


            if '185.51.200.1' in item:
                is_shecanPrivate2 = True

            if '1.1.1.1'  in item:
                is_VPN = True


        if is_noDNS and not(is_shecanPrivate1 or is_shecanPrivate2 or is_VPN):
            return ('no DNS')
        elif is_shecanPrivate1 and is_shecanPrivate2:
            return ('private shecan')
        elif is_VPN :
            return('VPN')

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
