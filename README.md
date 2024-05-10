# Flare Watcher Project README

## Overview
Flare Watcher is an innovative fire detection system that combines environmental sensors and advanced machine learning algorithms to detect and predict fire occurrences in real-time. Utilizing both sensor data and image analysis, this system provides a comprehensive solution for monitoring and responding to fire threats.

## Sensor Details

### Sensors Used

1. **SGP30 Sensor for TVOC and eCO2 Measurement**
   - **Type:** Gas sensor
   - **Purpose:** Measures Total Volatile Organic Compounds (TVOC) and equivalent Carbon Dioxide (eCO2) to detect the presence of fire-related compounds.
   - **Usage:** Continuously monitors air quality for chemical changes indicative of combustion.
   - [Datasheet for SGP30](https://www.sensirion.com/media/documents/984E0DD5/61644B8B/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf)

2. **SHT31 Sensor for Humidity Measurement**
   - **Type:** Humidity sensor
   - **Purpose:** Measures the relative humidity, where a sudden drop may indicate a nearby fire.
   - **Usage:** Assists in assessing environmental conditions to corroborate other fire indicators.
   - [Datasheet for SHT31](https://www.tme.eu/Document/2e0098c5e5c9e7ad6b9934b65a407be3/Sensirion_SHT3x_analog.pdf)

3. **BME280 Sensor for Pressure Measurement**
   - **Type:** Atmospheric pressure sensor
   - **Purpose:** Monitors atmospheric pressure; significant fluctuations can relate to weather changes or fires.
   - **Usage:** Provides insight into meteorological conditions and potential fire behavior.
   - [Datasheet for BME280](https://www.mouser.com/datasheet/2/783/BST-BME280-DS002-1509607.pdf)

4. **KY-026 Flame Detection Sensor**
   - **Type:** Infrared flame sensor
   - **Purpose:** Directly detects the presence of flames by sensing the infrared light emitted by fire.
   - **Usage:** Offers immediate detection of fires, enhancing the system's responsiveness.
   - [Datasheet for KY-026](https://moviltronics.com/wp-content/uploads/2019/10/KY-026.pdf)

### Machine Learning Models

1. **Random Forest Classification**
   - **Purpose:** Uses sensor data (TVOC, eCO2, humidity, pressure, and flame detection) to predict the likelihood of a fire.
   - **Implementation:** Trained with historical sensor data, learning to identify conditions indicative of fire.

2. **Convolutional Neural Networks (CNN)**
   - **Purpose:** Detects signs of fire in images by recognizing features such as smoke and flames.
   - **Implementation:** Trained on a dataset with 'fire' and 'no fire' images, improving the system’s visual detection capabilities.

## Installation and Setup

### Django setup
1. Install [python](https://www.python.org/downloads/)
2. Clone project and Install python virtual environment.
```
   git clone https://github.com/GGWPXXXX/Flare-Watcher
```
```
   python -m pip install virtualenv
```
3. Create a new .env file in the project's root directory. You can use a text editor of your choice to create and edit the file, you can see the sameple in sample.env.
4. Create new environment.
```
   python -m venv venv
```
5. Run this command to anable virtual environment.
```
   venv\Scripts\activate
```
6. Use the following command to install necessary dependencies.
```
   pip install -r requirements.txt
```
7. Run the program.
```
   python manage.py migrate
   python manage.py runserver
```
8. If you want to exit the program simply hit ctrl+c to deactivate django server and use
```
deactivate
```
   in your terminal to exit virtual environment.

### Mobile setup 
1. You'll need to download MQTT Camera application file via this  [link](https://colab.research.google.com/drive/133wTb-eIgVhNMxCE9WFQnDqw4xx3qokF?usp=sharing).
2. After you download it, Open the application and head to the settings to set up your MQTT connection.
3. Inside setting page you'll see the UUID menu, Click copy and paste it into your .env and config.py

### Line setup 
1. You'll need to create line official account via this [link](https://help.line.me/official_account_jp/ios/categoryId/20008250/pc?contentId=20013136).
2. Then go to LINE Developer [website](https://developers.line.biz/) and login with the same account of line that you use to create line official account.
3. After that goto Messaging API and scroll down until you see Channel access token. Copy and paste it into your .env file.

### Amazon S3 setup 
1. You'll need to create Amazon AWS, you can follow these [instruction](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
2. Lastly copy AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, and BUCKET_NAME into your .env file.


### Hardware setup
1. Connect the SGP30, SHT31, BME280, and KY-026 sensors to your microcontroller as per the respective datasheets.
2. Ensure a stable power supply and secure connections to avoid data interruptions.

## Usage

1. Calibrate each sensor according to the manufacturer's instructions for accurate readings.
2. Continuously collect data from the sensors and analyze it using the Random Forest model to assess fire likelihood.
3. Use cameras to capture area images, analyzing them with the CNN model for visual indications of fire.
4. Set up alerts and notifications to inform personnel or authorities when a fire is detected or predicted.

## Contributing

Contributions to the Flare Watcher project are welcome, including improvements to the machine learning models, sensor integration, and system enhancements. Please submit pull requests or issues through this repository.

## Additional

If you want to see the unit tests of this project simply run,
```
   python manage.py test
```
Note : Make sure that when you run test you still in virtual environment.

## Contact
For more information or inquiries, please contact [Flare Watcher Support](mailto:chaiyawut.t@ku.th).
