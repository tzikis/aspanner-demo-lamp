import time
import Spanner
from Testboard import Testboard

testboard = Testboard("Testboard1")

# Our Product's Input will be connected the Testboard's Pin D3, making it our
# Output Pin
OUTPUT_PIN = "D3"

INPUT_PIN_0 = "A0"
INPUT_PIN_1 = "A1"
INPUT_PIN_2 = "A2"
INPUT_PIN_3 = "A3"

def toggle_digital_output():
    # set PIN state
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'LOW')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')

if __name__ == "__main__":
    toggle_digital_output()
    Spanner.assertTrue(True)

    value = testboard.analogRead(INPUT_PIN_0)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_1)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_2)
    print("Read analog value: ","%d" % value, flush=True)
    value = testboard.analogRead(INPUT_PIN_3)
    print("Read analog value: ","%d" % value, flush=True)