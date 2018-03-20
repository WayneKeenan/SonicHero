from sys import argv
from sonicpi_osc import SonicPiOSCClient
from guitarhero_ble import BLEGuitar

if len(argv)<2:
    print("Specify a BluetoothLE address, e.g. F3:13:81:8B:37:00")
    exit(1)

device_addr = argv[1]       # Device Name in BLE scan: 'Ble Guitar'

sonicpi_osc = SonicPiOSCClient(path='/bubbleworks/bleguitar')

def on_guitar_message(guitar_state):
    sonicpi_osc.send([
        guitar_state['L1_pressed'],
        guitar_state['L2_pressed'],
        guitar_state['L3_pressed'],
        guitar_state['U1_pressed'],
        guitar_state['U2_pressed'],
        guitar_state['U3_pressed'],
        guitar_state['strummer'],
        guitar_state['whammy'],
        guitar_state['rotation_digital'],
        guitar_state['hero_power_pressed'],
        guitar_state['square_pressed'],
        guitar_state['connect_pressed'],
    ])

ble_guitar = BLEGuitar(device_addr=device_addr)
ble_guitar.on_guitar_message = on_guitar_message
ble_guitar.start()


