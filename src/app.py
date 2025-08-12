from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QMainWindow, QLabel, QComboBox,
                             QPushButton, QLineEdit, )
from traitlets.config import Config

from dns_util import check_dns

# main window structure
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #reading DNS
        self.status = check_dns()


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

        # first Section
        dns_first_row = QHBoxLayout()
        dns_first_row.addWidget(self.dns)
        dns_first_row.addWidget(self.dns_get)

        dns_second_row = QHBoxLayout()
        dns_second_row.addWidget(self.alt_dns)
        dns_second_row.addWidget(self.alt_dns_get)

        adapter_combo_box = QComboBox()
        adapter_combo_box.addItems(['Ethernet',])
        #setting GET_LABELs text
        self.dns_get.setText(self.status)
        self.alt_dns_get.setText(self.status)
        # Place first section
        first_section_box_layout = QVBoxLayout()
        first_section_box_layout.addLayout(dns_first_row)
        first_section_box_layout.addLayout(dns_second_row)
        first_section_box_layout.addWidget(adapter_combo_box)


        # Second Section
        if self.status=='no DNS':
            self.conn_btn = QPushButton(text='Connect')
        elif self.status == 'VPN':
            self.conn_btn = QPushButton(text='DISABLE VPN!')
            self.conn_btn.setEnabled(False)
        elif self.status=='private shecan':
            self.conn_btn = QPushButton(text='DisConnect')

        self.config_btn = QPushButton(text='Configure')
        self.config_btn.clicked.connect(self.config_btn_func)
        second_section_box_layout = QVBoxLayout()
        second_section_box_layout.addWidget(self.conn_btn)
        second_section_box_layout.addWidget(self.config_btn)



        main_layout = QVBoxLayout()
        main_layout.addLayout(first_section_box_layout)
        main_layout.addLayout(second_section_box_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)  # ← THIS is important
        self.cfg_window = None

    def conn_btn_click(self,):
        """
        Bottom to Connect OR Disconnect DNS
        :return:
        """
        pass

    def config_btn_func(self, click):
        """
        Show Configur WIndow
        :return:
        """
        self.cfg_window = ConfigWindow()
        self.cfg_window.show()

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Config')
        self.title_line = QLabel(text='Insert New DNS Below')

        self.dns_line = QLabel(text='DNS:')
        self.dns_input = QLineEdit()
        self.alt_dns_line = QLabel(text='Alternate DNS:')
        self.alt_dns_input = QLineEdit()

        self.confirm_btn = QPushButton(text='Confirm',)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.dns_line)
        hbox1.addWidget(self.dns_input)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.alt_dns_line)
        hbox2.addWidget(self.alt_dns_input)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.confirm_btn)
        self.setLayout(vbox)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
