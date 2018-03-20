# SonicHero

A quick little hack allowing the control of Sonic Pi using a GuitarHero Wireless Guitar (Bluetooth LE version).



## Hardware

You will need a Pi3 or Pi Zero W, or another type of Pi with a Bluetooth LE USB dongle.

You can find the GuitarHero Live Guitar available for about 10 UK Pounds online (e.g. Amazon, while stocks last) and retail outlets (e.g. Maplins, while they last!).


## Install

```bash
sudo pip3 install bluezero python-osc
git clone https://github.com/WayneKeenan/SonicHero.git

```

## Setup

Find and connect to the controller.

In a shell on the Pi launch the `bluetoothctl` shell:

```
bluetoothctl
scan on
scan off
```

You should see you GuitarHero controller appear as 'Ble guitar', e.g.:

```
[NEW] Device F3:13:81:8B:37:00 Ble Guitar
```

The `F3:13:81:8B:37:00` is the DEVICE_ADDRESS, it will be used in the next few sections, replace as necessary.

While still in the `bluetoothctl` shell type:
```
trust DEVICE_ADDRESS
connect DEVICE_ADDRESS
exit
```

You may have to repeat the above if you find you can't connect in the future.

## Running

On the Pi desktop launch SonicPi and past in the constest of the [sonicpi_example.rb](sonicpi_example.rb) script.

In a terminal on the Pi run:

```bash
cd SonicHero
python3 bleguitar_agent.py DEVICE_ADDRESS
```

