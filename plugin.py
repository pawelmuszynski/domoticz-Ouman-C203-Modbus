#!/usr/bin/env python


"""
Ouman C203 regulator. The Python plugin for Domoticz
Author: pawelmuszynski
Requirements:
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="Ouman-C203" name="Ouman-C203-Modbus" version="0.0.1" author="pawelmuszynski">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600" />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="11" />
        <param field="Mode3" label="Reading Interval sec." width="40px" required="true" default="60" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug" />
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""


import minimalmodbus
import Domoticz


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = ""
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False

        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("Ouman C203 Modbus plugin start")
        self.runInterval = int(Parameters["Mode3"]) / 60
        if 1 not in Devices:
            Domoticz.Device(Name="Supply temperature", Unit=1, TypeName="Temperature", Used=0).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="Return temperature", Unit=2, TypeName="Temperature", Used=0).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="Outdoor temperature", Unit=3, TypeName="Temperature", Used=0).Create()
        if 4 not in Devices:
            Domoticz.Device(Name="Output voltage", Unit=4, TypeName="Voltage", Used=0).Create()

    def onStop(self):
        Domoticz.Log("Ouman C203 Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from Ouman C203
            try:
                supplyTemp    = self.rs485.read_register(registeraddress=203, functioncode=3, signed=True, number_of_decimals=1)
                returnTemp    = self.rs485.read_register(registeraddress=205, functioncode=3, signed=True, number_of_decimals=1)
                outdoorTemp   = self.rs485.read_register(registeraddress=1493, functioncode=3, signed=True, number_of_decimals=1)
                outputVoltage = self.rs485.read_register(registeraddress=236, functioncode=3, signed=True, number_of_decimals=2)

            except:
                Domoticz.Log("Connection problem");
            else:
                #Update devices
                Devices[1].Update(0,str(supplyTemp))
                Devices[2].Update(0,str(returnTemp))
                Devices[3].Update(0,str(outdoorTemp))
                Devices[4].Update(0,str(outputVoltage))


            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("Ouman C203 Modbus Data")
                Domoticz.Log('Supply temperature: {0:.1f} °C'.format(supplyTemp))
                Domoticz.Log('Return temperature: {0:.1f} °C'.format(returnTemp))
                Domoticz.Log('Outdoor temperature: {0:.1f} °C'.format(outdoorTemp))
                Domoticz.Log('Output voltage: {0:.2f} V'.format(outputVoltage))

        self.runInterval = int(Parameters["Mode3"]) * 0.1

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()


# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
