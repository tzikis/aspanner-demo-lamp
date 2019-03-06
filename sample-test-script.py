import sys
import time
import Spanner
from Testboard import Testboard

import http.client, urllib.parse
import json

testboard = Testboard("Testboard1")

particle_token = "b4992ee32f43c39c8ea4fa0a178672c72f5dead8"
device_id = "370053000351353530373132"

raspberry_base_url = "bdf89d03d3e0cf7d0292bfc097193890.balena-devices.com"

# Our Product's Input will be connected the Testboard's Pin D3, making it our
# Output Pin
OUTPUT_PIN = "D3"

RELAY_PIN = "A5"

INPUT_PIN_RED = "A3"
INPUT_PIN_GREEN = "A2"
INPUT_PIN_BLUE = "A1"
INPUT_PIN_WHITE = "A0"


def turn_ap_on():
    print("#### Setting WiFi Access Point On ####")
    return_val = send_raspberry_command("wifion")
    if(!return_val):
        sys.exit(1)
    print("####    Access Point Set to On    ####")

def turn_ap_off():
    print("#### Setting WiFi Access Point Off ####")
    send_raspberry_command("wifioff")
    if(!return_val):
        sys.exit(1)
    print("####    Access Point Set to Off    ####")

def send_raspberry_command(command_string):
    resource_uri = "/" + command_string + '?rand=' + "201"

    conn = http.client.HTTPSConnection(raspberry_base_url)

    # print("=== Sending AP Command ===")
    # print("URL: https://" + raspberry_base_url + resource_uri)

    conn.request('GET', resource_uri)

    response = conn.getresponse()
    # print("=== Raw Response ===")
    response = response.read().decode()
    # print(response)
    # print("====================")

    return (response == "OK")

def toggle_digital_output():
    # set PIN state
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'LOW')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')


def toggle_relay():
    # set PIN state
    testboard.digitalWrite(RELAY_PIN, 'LOW')
    time.sleep(2)
    testboard.digitalWrite(RELAY_PIN, 'HIGH')
    time.sleep(5)
    testboard.digitalWrite(RELAY_PIN, 'LOW')
    time.sleep(2)


def sendParticleCommand(auth_token, device, command, value):
    base_url = 'api.particle.io'
    api_path = '/v1/devices/'
    resource_uri =  api_path + device + '/' + command

    conn = http.client.HTTPSConnection(base_url)
    headers = {'Authorization': 'Bearer ' + auth_token, "Content-type": "application/x-www-form-urlencoded"}
    params = urllib.parse.urlencode({'@arg': value})

    # print("=== Sending Particle Command ===")
    # print("URL: https://" + base_url + resource_uri)
    # print("Params: " + params)
    # print("=== Headers ===")
    # print(headers)

    conn.request('POST', resource_uri, params, headers)

    response = conn.getresponse()
    # print("=== Raw Response ===")
    response = response.read().decode()
    # print(response)
    # print("====================")
    json_obj = json.loads(response)

    return json_obj["return_value"]

def setDeviceColor(color):
    print("$$$$ Setting Device Color $$$$")
    print("New Color: " + color)    
    return_code = sendParticleCommand(particle_token, device_id, "setColor", color)
    if(return_code != 1):
        sys.exit(1)
    print("$$$$   Successfully Set   $$$$")

def setDeviceOn():
    print("$$$$ Setting Device On $$$$")
    return_code = sendParticleCommand(particle_token, device_id, "setOnOff", "1")
    if(return_code != 1):
        sys.exit(1)
    print("$$$$ Successfully Set  $$$$")

def setDeviceOff():
    print("$$$$ Setting Device Off $$$$")
    return_code = sendParticleCommand(particle_token, device_id, "setOnOff", "0")
    if(return_code != 0):
        sys.exit(1)
    print("$$$$  Successfully Set  $$$$")

def testDeviceOffLEDs():
    time.sleep(2)
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(300, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(300, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(300, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(300, value);

def testDeviceColorAllFullLEDs():
    time.sleep(2)
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(3700, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(3700, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(3700, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(3700, value);

def testDeviceButtonToggleOnOffOn():
    setDeviceColor("ffffffff")

    testDeviceColorAllFullLEDs()
    toggle_digital_output()

    testDeviceOffLEDs()

    toggle_digital_output()

    testDeviceColorAllFullLEDs()

def testDeviceButtonToggleOnOffOnWithoutWifi():
    setDeviceColor("ffffffff")

    testDeviceColorAllFullLEDs()

    turn_ap_off()

    time.sleep(5)

    toggle_digital_output()

    testDeviceOffLEDs()

    toggle_digital_output()

    testDeviceColorAllFullLEDs()

    turn_ap_on()


def testDeviceRebootKeepsLEDOn():
    setDeviceColor("ffffffff")
    time.sleep(2)

    testDeviceColorAllFullLEDs()

    toggle_relay()
    time.sleep(1)
    
    testDeviceColorAllFullLEDs()

def testDeviceRebootKeepsLEDOff():
    setDeviceOff()
    time.sleep(2)

    testDeviceOffLEDs()

    toggle_relay()
    time.sleep(1)
    
    testDeviceOffLEDs()

if __name__ == "__main__":

    turn_ap_on()
    time.sleep(20)

    setDeviceOff()
    testDeviceOffLEDs()

    time.sleep(5)
    
    setDeviceColor("ffffffff")
    testDeviceColorAllFullLEDs()

    time.sleep(5)
    
    testDeviceButtonToggleOnOffOn()

    time.sleep(5)

    testDeviceRebootKeepsLEDOn()

    time.sleep(10)

    testDeviceRebootKeepsLEDOff()

    testDeviceButtonToggleOnOffOnWithoutWifi()



