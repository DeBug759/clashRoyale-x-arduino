import urllib.request
import json
from time import sleep
import pyfirmata
import time

arduino = pyfirmata.Arduino('COM3')


def get_data():
    with open("Resources/my_key.txt") as f:
        my_key = f.read().rstrip("\n")

        base_url = "https://api.clashroyale.com/v1"
        endpoint = "/players/"
        # Aslan's playerTag = "%23R9VL20G9"
        # Runbier's playerTag = "%23R0C0JGJY8"
        # Krithik's
        playerTag = "%23UL0QQ999G"
        # playerTag = "%23R0C0JGJY8"

        request = urllib.request.Request(
            base_url + endpoint + playerTag,
            None,
            {
                "Authorization": "Bearer %s" % my_key
            }
        )

        data = urllib.request.urlopen(request).read().decode("utf-8")

        json_string = json.dumps(data)

        with open('json_data.json', 'w') as outfile:
            outfile.write(json_string)

        obj = json.loads(data)

        wins = int(str(obj["wins"]))
        threeCrownWins = int(str(obj["threeCrownWins"]))

        losses = int(str(obj["losses"]))

        print("---------------------------")
        print("Wins: " + str(wins))
        # print("Three crown wins: " + str(threeCrownWins))
        print("Losses: " + str(losses))
        print("---------------------------")
        sleep(10)

        return obj, wins, threeCrownWins, losses


obj, wins, threeCrownWins, losses = get_data()

pin = 4
def rotateServo(pin, angle):
    arduino.digital[pin].write(angle)
    sleep(0.015)


while True:

    obj = get_data()[0]

    if int(str(obj["wins"])) > wins:
        print("You won a game!")
        arduino.digital[8].write(1)
        time.sleep(20)

        # Servo pin
        pin = 4

        for i in range(0, 180):
            rotateServo(pin, i)
        for i in range(180, 1, -1):
            rotateServo(pin, i)

        break

    elif int(str(obj["threeCrownWins"])) > threeCrownWins:
        print("You got a THREE CROWN WIN!")
        arduino.digital[8].write(1)
        time.sleep(0.5)
        arduino.digital[8].write(0)
        time.sleep(0.5)
        arduino.digital[8].write(1)
        time.sleep(5)
        arduino.digital[8].write(0)
        break

    elif int(str(obj["losses"])) > losses:

        print("You lost a game!")
        arduino.digital[7].write(1)
        time.sleep(5)
        arduino.digital[7].write(0)
        break

    print(f"Wins: {int(str(obj['wins']))}")
    print(f"Losses: {int(str(obj['losses']))}")