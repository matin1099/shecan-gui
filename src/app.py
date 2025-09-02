import subprocess,os , sys
from loguru import logger as log
import configparser
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QMainWindow, QLabel, QComboBox,
                             QPushButton, QLineEdit, )

from src import config
from src.dns_util import check_dns
from src.shecan_util import clean_shecan, shecan






#########
###UNCOMMENT FOR other level####
log.remove()
###### uncomment  JUST ONE!!!!!!!!!!!!!!!
# log.add(sys.stderr, level="TRACE")  # MOST OF EVENTS
#log.add(sys.stderr, level="DEBUG")  # DEFAULT
# log.add(sys.stderr, level="INFO")   # LESS LOG
# log.add(sys.stderr, level="SUCCESS")# GOOD NEWS ONLY
# log.add(sys.stderr, level="WARNING")# I LIKE IT UNTOLD!!
# log.add(sys.stderr, level="ERROR")  # REASONS TO CALL MATIN!!!
# log.add(sys.stderr, level="CRITICAL")# JUST NOTIFY ME IN DANGER
#########




# main window structure
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.status = check_dns()

        ### this section rewrite by a config reader funcs
        self.dns_add = "78.22.122.101"
        self.alt_dns_add = "185.51.200.1"



        self.setWindowTitle('Shecan')



        # first container
        # Contain three line two column
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

        self.conn_btn = QPushButton(text='Connect')

        # Second Section
        if self.status=='no DNS':
            self.conn_btn.setText('Connect')
        elif self.status == 'VPN':
            self.conn_btn.setText('DISABLE VPN!')
            self.conn_btn.setEnabled(False)
        elif self.status=='private shecan':
            self.conn_btn.setText('DisConnect')

        self.conn_btn.clicked.connect(self.conn_btn_click)

        self.config_btn = QPushButton(text='Configure')
        self.config_btn.clicked.connect(self.config_btn_func)


        second_section_box_layout = QVBoxLayout()
        second_section_box_layout.addWidget(self.conn_btn)
        # second_section_box_layout.addWidget(self.config_btn)



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
        if self.conn_btn.text() == 'Connect':
            log.info("IT IS CONNECT")
            shecan(self.dns_add, self.alt_dns_add,adapter='Ethernet')
            self.conn_btn.setText('DisConnect')

        elif self.conn_btn.text() == 'DisConnect':
            log.info("IT IS DisCONNECT")
            clean_shecan(adapter='Ethernet')
            self.conn_btn.setText('Connect')

        self.status = check_dns()
        log.info('readed new status ')
        self.dns_get.setText(self.status)
        log.info('dns new status ')
        self.alt_dns_get.setText(self.status)
        log.info('dnsalt new status ')

    def config_btn_func(self, click):
        """
        Show Configur WIndow
        :return:
        """
        if self.cfg_window is None:
            pass
            # self.cfg_window = ConfigWindow()
        # self.cfg_window.show()

# class ConfigWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         config = configparser.ConfigParser()
#         config.read('dns.ini')
#         cfg_prof_list = config.sections()
#
#         self.setWindowTitle('Configure DNS')
#
#
#         self.profile_dns = QLabel(text='Profile:')
#         self.profile_combo_box = QComboBox()
#         self.profile_combo_box.addItems(cfg_prof_list)
#         self.dns_line = QLabel(text='DNS:')
#         self.dns_input = QLineEdit()
#         self.alt_dns_line = QLabel(text='Alternate DNS:')
#         self.alt_dns_input = QLineEdit()
#
#         self.confirm_btn = QPushButton(text='Confirm',)
#         self.confirm_btn.clicked.connect(self.close)
#
#         hbox1 = QHBoxLayout()
#         hbox1.addWidget(self.profile_dns)
#         hbox1.addWidget(self.profile_combo_box)
#         hbox2 = QHBoxLayout()
#         hbox2.addWidget(self.dns_line)
#         hbox2.addWidget(self.dns_input)
#         hbox3 = QHBoxLayout()
#         hbox3.addWidget(self.alt_dns_line)
#         hbox3.addWidget(self.alt_dns_input)
#         vbox = QVBoxLayout()
#         vbox.addLayout(hbox1)
#         vbox.addLayout(hbox2)
#         vbox.addLayout(hbox3)
#         vbox.addWidget(self.confirm_btn)
#         self.setLayout(vbox)
if __name__=='__main__':
    configFile = config.config_reader()
    #print(configFile)
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
