from time import sleep
import logging
from bluezero import adapter, central
from binascii import b2a_hex

from struct import unpack

dongle = adapter.Adapter(adapter.list_adapters()[0])
LOGGER = logging.getLogger(__name__)


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


class BLEGuitar:

    BLE_GUITAR_SERVICE = '533E1523-3ABE-F33F-CD00-594E8B0A8EA3'
    BLE_GUITAR_CHAR = '533E1524-3ABE-F33F-CD00-594E8B0A8EA3'

    def __init__(self, device_addr, adapter_addr=dongle.address):
        self._guitar = central.Central(adapter_addr=adapter_addr, device_addr=device_addr)
        self._guitar_rx = self._guitar.add_characteristic(BLEGuitar.BLE_GUITAR_SERVICE, BLEGuitar.BLE_GUITAR_CHAR)
        self.on_connect = lambda x : None
        self.on_guitar_message = lambda x : None
        self.last_dict = {}

    def connect(self):
        self._guitar.connect()
        LOGGER.debug("Connected")
        while not self._guitar.services_resolved:
            sleep(0.5)
        LOGGER.debug("GATT services resolved")
        self._guitar.load_gatt()

    def disconnect(self):
        self._guitar.disconnect()

    def _on_message(self, dbus_gatt_char, dbus_data, some_dbus_array):
        if 'Value' in dbus_data:
            value = dbus_data['Value']
            data  =  bytearray([int(c) for c in value])
            self.on_message(data)

    def subscribe_rx(self, user_callback):
        self._guitar_rx.add_characteristic_cb(self._on_message)
        self._guitar_rx.start_notify()

    def start(self):
        self.connect()
        self.subscribe_rx(self.on_message)
        self._guitar.run()


    def on_message(self, data):
        LOGGER.debug(b2a_hex(data))
        values = (
            buttons_1,
            buttons_2,
            dpad,
            _,
            strummer,
            rotation_digital,
            whammy,
            x, y, z,  # ? ? ? ,  Z is bat? last reading:  01 08 df
            rotation
        ) = unpack("BBBBBBBxxxxxxxxxBBBB", data)

        LOGGER.debug(values)
        dpad_state = 0 if dpad == 0x0F else dpad + 1
        whammy -= 0x80

        if rotation_digital == 0x00:            # Down
            rotation_digital = -1
        elif rotation_digital == 0xFF:          # Up
            rotation_digital = 1
        else:
            rotation_digital = 0                # Level

        if strummer == 0xFF:            # Down
            strummer = -1
        elif strummer == 0x00:          # Up
            strummer = 1
        else:
            strummer = 0                # Level


        message = dict(
            L1_pressed = bool(buttons_1 & 0x01),
            L2_pressed = bool(buttons_1 & 0x10),
            L3_pressed = bool(buttons_1 & 0x20),
            U1_pressed = bool(buttons_1 & 0x02),
            U2_pressed = bool(buttons_1 & 0x04),
            U3_pressed = bool(buttons_1 & 0x08),
            strummer = strummer,
            whammy=whammy,
            rotation_digital=rotation_digital,
            hero_power_pressed = bool(buttons_2 & 0x08),
            dpad= dpad_state,
            square_pressed = bool(buttons_2 & 0x04),
            connect_pressed = bool(buttons_2 & 0x10),
            #rotation=rotation,                         # ignore...
        )

        # Only send delta's, ignoring rotation as it overwhelms SonicPi
        (added, removed, modified, same) = dict_compare(self.last_dict, message)
        if len(modified):
            self.on_guitar_message(message)
        self.last_dict = message.copy()

"""
BLE Guitar Input Mappings

buttons_1 
 0x00   None
 0x01   L1
 0x02   U1
 0x04   U2
 0x08   U3
 0x10   L2
 0x20   L3

buttons_2
 0x00   None
 0x04   Square pressed
 0x10   'Connect'  pressed
 0x08   Hero power pressed

dpad
 0x0f   None
 0x00   N
 0x01   NW
 0x02   W
 0x03   SW
 0x04   S
 0x05   SE
 0x06   E
 0x07   NE

strummer
  0x00 = Up 
  0x80 = Rest  
  0xFF = Down

whammy (Analog)
  0x80 = Rest
   ..
  0xFF = Full on   

rotation_digital (digital)
  0x00  Headstock pointing down
  0x80  Headstock level
  0xFF  Headstock pointing up


rotation (Analog)

  0x00  Headstock pointing down
   ..
  0x80  Headstock level
   ..
  0xFF  Headstock pointing up
"""
