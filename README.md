# domoticz-Ouman-C203-Modbus
## Description
Ouman C203 regulator with RS485 Port modbus RTU for Domoticz plugin.

Modbus plugin for YONY heat meter. For now it supports Supply temperature,
Return temperature and Outside temperature values only.
Registers has been found by reverse engineering.

## Hardware and wiring
Tested with chinese RS485 to USB module.

## Installation
```
cd ~/domoticz/plugins
pip install -r requirements.txt
git clone https://github.com/pawelmuszynski/domoticz-Ouman-C203-Modbus
```
Restart your Domoticz server.

## Used modules
- minimalmodbus 2.0.1

Tested with Domoticz 2023.1.
