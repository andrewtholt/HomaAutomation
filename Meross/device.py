#!/usr/bin/env python3
import os
import time
from random import randint
import sys

from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener
from meross_iot.cloud.devices.hubs import GenericHub
from meross_iot.cloud.devices.humidifier import GenericHumidifier, SprayMode
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.subdevices.thermostats import ValveSubDevice, ThermostatV3Mode
from meross_iot.cloud.devices.subdevices.sensors import SensorSubDevice
from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

name = set()

def event_handler(eventobj):
    if eventobj.event_type == MerossEventType.DEVICE_ONLINE_STATUS:
        print("Device online status changed: %s went %s" % (eventobj.device.name, eventobj.status))
        pass

    elif eventobj.event_type == MerossEventType.DEVICE_SWITCH_STATUS:
        print("Switch state changed: Device %s (channel %d) went %s" % (eventobj.device.name, eventobj.channel_id,
                                                                        eventobj.switch_state))
    elif eventobj.event_type == MerossEventType.CLIENT_CONNECTION:
        print("MQTT connection state changed: client went %s" % eventobj.status)

        # TODO: Give example of reconnection?

    elif eventobj.event_type == MerossEventType.GARAGE_DOOR_STATUS:
        print("Garage door is now %s" % eventobj.door_state)

    elif eventobj.event_type == MerossEventType.THERMOSTAT_MODE_CHANGE:
        print("Thermostat %s has changed mode to %s" % (eventobj.device.name, eventobj.mode))

    elif eventobj.event_type == MerossEventType.THERMOSTAT_TEMPERATURE_CHANGE:
        print("Thermostat %s has revealed a temperature change: %s" % (eventobj.device.name, eventobj.temperature))

    elif eventobj.event_type == MerossEventType.SENSOR_TEMPERATURE_CHANGE:
        print("Sensor %s has revealed a temp/humidity change: %s %s" % (eventobj.device.name, eventobj.temperature, eventobj.humidity))

    elif eventobj.event_type == MerossEventType.SENSOR_TEMPERATURE_ALERT:
        print("Sensor %s has revealed a temperature alert: %s" % (eventobj.device.name, eventobj.alert))

    else:
        print("Unknown event!")


if __name__ == '__main__':
    # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
    manager = MerossManager(meross_email=EMAIL, meross_password=PASSWORD)

    # Register event handlers for the manager...
    manager.register_event_handler(event_handler)

    # Starts the manager
    manager.start()

    # You can retrieve the device you are looking for in various ways:
    # By kind
    all_devices = manager.get_supported_devices()


    print("All the hub devices I found:")
    for d in all_devices:
#        print(d)
        print(d.name)
        dir(d)
        name.add( d.name )

    sys.exit(0)
    # You can also retrieve devices by the UUID/name
    # a_device = manager.get_device_by_name("My Plug")
    # a_device = manager.get_device_by_uuid("My Plug")
    # Or you can retrieve all the device by the HW type
    # all_mss310 = manager.get_devices_by_type("mss310")
    # ------------------------------
    # Let's play the garage openers.
    # ------------------------------
