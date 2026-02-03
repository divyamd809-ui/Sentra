import requests
import time

def test():

    tries = 0

    for _ in range(20):

        try:

            requests.get("https://9vqhg29w-5000.inc1.devtunnels.ms/admin")
            time.sleep(20)

            tries += 1

        except Exception as e:

            print(e)

test()