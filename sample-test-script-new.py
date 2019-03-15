

import pytest
import time
from Testboard import Testboard

import http.client, urllib.parse
import json

from random import randint


# Our Product's Input will be connected the Testboard's Pin D3, making it our
# Output Pin
OUTPUT_PIN = "D3"

RELAY_PIN = "A5"

INPUT_PIN_RED = "A3"
INPUT_PIN_GREEN = "A2"
INPUT_PIN_BLUE = "A1"
INPUT_PIN_WHITE = "A0"

testboard = Testboard("Testboard1")


class Device:

    BASE_URL = 'api.particle.io'
    API_PATH = '/v1/devices/'

    def __init__(self, device_id, token):
        self.device_id = device_id
        self.token = token

    def cmd(self, command, value):
        resource_uri = Device.API_PATH + self.device_id + '/' + command

        conn = http.client.HTTPSConnection(Device.BASE_URL)
        headers = {'Authorization': 'Bearer ' + self.token, "Content-type": "application/x-www-form-urlencoded"}
        params = urllib.parse.urlencode({'@arg': value})
        conn.request('POST', resource_uri, params, headers)

        response = conn.getresponse()
        response = response.read().decode()
        json_obj = json.loads(response)
        return json_obj["return_value"]

    def setOn(self):
        print("$$$$ Setting Device On $$$$")
        return_code = self.cmd("setOnOff", "1")
        if return_code != 1:
            pytest.fail("Failed to set device on")
        print("$$$$ Successfully Set  $$$$")

    def setOff(self):
        print("$$$$ Setting Device Off $$$$")
        return_code = self.cmd("setOnOff", "0")
        if return_code != 0:
            pytest.fail("Failed to set device off")
        print("$$$$  Successfully Set  $$$$")

    def setColor(self, color):
        print("$$$$ Setting Device Color $$$$")
        print("New Color: " + color)
        return_code = self.cmd("setColor", color)
        if return_code != 1:
            pytest.fail("Failed to set device color")
        print("$$$$   Successfully Set   $$$$")




@pytest.fixture(scope='module')
def device():
    print("++++ Turning Device On ++++")
    testboard.digitalWrite(RELAY_PIN, 'HIGH')
    time.sleep(30)
    print("++++        Done       ++++")

    particle_token = "b4992ee32f43c39c8ea4fa0a178672c72f5dead8"
    device_id = "370053000351353530373132"

    yield Device(device_id, particle_token)

    print("++++ Turning Device Off ++++")
    testboard.digitalWrite(RELAY_PIN, 'LOW')
    time.sleep(2)
    print("++++        Done        ++++")


def toggle_digital_output():
    # set PIN state
    print("++++ Simulating Button Press ++++")
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'LOW')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')
    print("++++           Done          ++++")


def toggle_relay():
    print("++++ Simulating Power Reset ++++")
    testboard.digitalWrite(RELAY_PIN, 'LOW')
    time.sleep(5)
    testboard.digitalWrite(RELAY_PIN, 'HIGH')
    time.sleep(2)
    print("++++          Done         ++++")


def myColorAssert(color):
    i = 0
    pins = [INPUT_PIN_RED, INPUT_PIN_GREEN, INPUT_PIN_BLUE, INPUT_PIN_WHITE]
    for pin in pins:
        value = testboard.analogRead(pin)
        print("Read analog value: ", "%d" % value, flush=True)
        if color[i:i+2] == 'ff':
            assert value > 3500
        else:
            assert value < 500
        i += 2


def test_programmatic_led_off_are_all_on(device):
    print("**** Testing LEDs Are all ON ****")
    color = "ffffffff"
    device.setColor(color)
    time.sleep(5)
    myColorAssert(color)
    print("****      Testing Done       ****")


def test_programmatic_led_off(device):
    print("**** Testing LEDs Turn off programmatically ****")
    device.setOff()
    time.sleep(5)
    myColorAssert("000000")
    print("****      Testing Done       ****")


def test_indepedent_led_color(device):
    print("<<<< Testing Independently Each LED >>>>")

    colors_codes = [('RED', 'ff000000'),
                    ('GREEN', '00ff0000'),
                    ('BLUE', '0000ff00'),
                    ('WHITE', '000000ff')]

    for color in colors_codes:
        print('**** Testing LED {} 100% ****'.format(color[0]))
        device.setColor(color[1])
        time.sleep(2)
        myColorAssert(color[1])

    print("****      Testing Done       ****")


def test_device_button_toggle_on_off(device):
    print("<<<< Testing Device Button Turns LED On/Off >>>>")
    color = "ffffffff"
    device.setColor(color)
    myColorAssert(color)

    toggle_digital_output()
    myColorAssert("00000000")

    toggle_digital_output()
    myColorAssert(color)
    print("<<<<              Testing Done              >>>>")


def test_device_reboot_keeps_led_on(device):
    print("<<<< Testing Reboot keeps LED On >>>>")

    color = "ffffffff"
    device.setColor(color)
    time.sleep(2)

    myColorAssert(color)

    toggle_relay()
    time.sleep(1)

    myColorAssert(color)
    print("<<<<        Testing Done         >>>>")


def test_device_reboot_keeps_led_off(device):
    print("<<<< Testing Reboot keeps LED Off >>>>")
    color = "00000000"
    device.setColor(color)
    time.sleep(2)

    myColorAssert(color)

    toggle_relay()
    time.sleep(1)

    myColorAssert(color)
    print("<<<<        Testing Done          >>>>")
