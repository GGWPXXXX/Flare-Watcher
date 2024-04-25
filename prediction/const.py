WARNING_MSG = """\
⚠️ Fire Alert ⚠️

Our monitoring system has detected potential signs of fire based on the readings from multiple sensors and models. Two out of three sources indicate the following:

🔥 Sensor Prediction: {}
🔥 Image Prediction: {}
🔥 Flame Sensor: {}

Please be vigilant and take necessary precautions. We recommend visually inspecting the area for any signs of smoke or flames.

If you confirm the presence of a fire, please evacuate immediately and contact the appropriate emergency services.

We will continue monitoring the situation and provide updates as necessary. Your safety is our top priority.

"""

ALERT_MSG = """\
🔥 Fire Emergency 🔥

Our monitoring system has detected a high likelihood of a fire based on the readings from all three sensors and models:

🚨 Sensor Prediction: {}
🚨 Image Prediction: {}
🚨 Flame Sensor: {}

Immediate evacuation is strongly recommended. Please leave the premises immediately and proceed to the designated safe area.

Emergency services have been notified, and assistance is on the way. Do not attempt to extinguish the fire yourself unless it is safe to do so.

We will continue to monitor the situation and provide updates as they become available. Your safety is our utmost concern.

"""


LIVE_DATA_NO_FIRE_MSG = """\
📷 Live Data - No Fire Detected 📷

Based on the latest data from our monitoring system, there is currently no fire detected in the monitored area. Here are the latest sensor readings:

🌡️ Humidity: {}%
🌫️ TVOC: {} ppb
🌬️ eCO2: {} ppm
☁️ Pressure: {} hPa
🔥 Flame Sensor: {}

Please note that these readings are subject to change, and we will continue to monitor the situation closely. If any concerning changes are detected, we will promptly notify you.

Stay safe, and thank you for using our fire monitoring service. Your safety is our top priority."""