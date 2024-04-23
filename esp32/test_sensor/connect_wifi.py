import network
import time

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if sta_if.isconnected():
    sta_if.disconnect()
time.sleep(1)
sta_if.connect("Chuchart__new2.4G", "024126838")