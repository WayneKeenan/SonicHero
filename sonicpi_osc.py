
# https://github.com/samaaron/sonic-pi/blob/master/etc/doc/tutorial/12.1-Receiving-OSC.md

# Python OSC Module: https://github.com/gkvoelkl/python-sonic
# sudo pip3 install python-sonic


from pythonosc import osc_message_builder
from pythonosc import udp_client

class SonicPiOSCClient:

    def __init__(self, path='/bubbleworks/default', address='127.0.0.1', port=4559):
        self.path = path
        self.sender = udp_client.UDPClient(address, port)

    def send(self, data):
        builder = osc_message_builder.OscMessageBuilder(address=self.path)

        for value in data:
            builder.add_arg(value, builder.ARG_TYPE_INT)

        msg = builder.build()
        self.sender.send(msg)


