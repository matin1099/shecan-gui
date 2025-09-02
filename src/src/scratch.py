# import configparser
#
# config = configparser.ConfigParser()
#
# config.read(open('setting.ini'))
# print(config.sections())
# #print(config['DEFAULT']['dns'])
# print(config)

import socket

# Return a list of network interface information
print(socket.if_nameindex())