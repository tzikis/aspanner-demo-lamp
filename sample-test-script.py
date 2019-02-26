import time
import Spanner
from Testboard import Testboard

import http.client, urllib.parse
import json

testboard = Testboard("Testboard1")

particle_token = "b4992ee32f43c39c8ea4fa0a178672c72f5dead8"
device_id = "370053000351353530373132"

# Our Product's Input will be connected the Testboard's Pin D3, making it our
# Output Pin
OUTPUT_PIN = "D3"

INPUT_PIN_RED = "A3"
INPUT_PIN_GREEN = "A2"
INPUT_PIN_BLUE = "A1"
INPUT_PIN_WHITE = "A0"

def toggle_digital_output():
    # set PIN state
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'LOW')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')


def setDeviceColor(color):
    conn = http.client.HTTPSConnection('api.particle.io')
    headers = {'Authorization': 'Bearer ' + particle_token, "Content-type": "application/x-www-form-urlencoded"}
    params = urllib.parse.urlencode({'@arg': "ff00ff00"}) #"arg=0040a0ff"

    conn.request('POST', '/v1/devices/' + device_id + '/setColor', params, headers)

    response = conn.getresponse()
    print(response.read().decode())

def setDeviceOn():
    conn = http.client.HTTPSConnection('api.particle.io')
    headers = {'Authorization': 'Bearer ' + particle_token, "Content-type": "application/x-www-form-urlencoded"}
    params = urllib.parse.urlencode({'@arg': "1"})

    conn.request('POST', '/v1/devices/' + device_id + '/setOnOff', params, headers)

    response = conn.getresponse()
    print(response.read().decode())

def setDeviceOff():
    conn = http.client.HTTPSConnection('api.particle.io')
    headers = {'Authorization': 'Bearer ' + particle_token, "Content-type": "application/x-www-form-urlencoded"}
    params = urllib.parse.urlencode({'@arg': "0"})

    conn.request('POST', '/v1/devices/' + device_id + '/setOnOff', params, headers)

    response = conn.getresponse()
    print(response.read().decode())


if __name__ == "__main__":
    toggle_digital_output()
    Spanner.assertTrue(True)

    setDeviceOff()
    sleep(2)
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)

    sleep(5)
    
    setDeviceOn()
    sleep(2)
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
