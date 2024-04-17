import urequests
import ubinascii
import urequests
import network
import upip
import os


try:
    import urequests
except ImportError:
    print("Installing urequests...")
    upip.install('urequests')
    import urequests

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if wlan.isconnected() == False:
    wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    print("Can't connect :(")
    sleep(0.5)
print("Connected!")

img = "C:/Users/patta/Downloads/pixlr-image-generator-ff22fce5-584c-4eda-967d-4c188a5e670f.png"
img_b64 = ubinascii.b2a_base64(img).decode('utf-8')
img_b64 += '=' * ((4 - len(img_b64) % 4) % 4)
print(img_b64)
url = 'http://127.0.0.1:8000/predict/image_prediction/'
data = {'image': img_b64}

try:
    response = urequests.post(url, data=data)
    print(response.status_code)
    
except OSError as e:
    print(f"Error sending request: {e}")
