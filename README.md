# Flare Watcher Project README

## Overview
Flare Watcher is an innovative fire detection system that integrates a network of sensors and utilizes advanced machine learning algorithms to detect and predict fire occurrences in real-time. This system uses both environmental data and image analysis to provide a comprehensive monitoring solution.

## Sensor Details

### Sensors Used

1. **SGP30 Sensor for TVOC and eCO2 Measurement**
   - **Type:** Gas sensor
   - **Purpose:** Measures Total Volatile Organic Compounds (TVOC) and equivalent Carbon Dioxide (eCO2) levels. These measurements can indicate the presence of fire when abnormal values are detected.
   - **Usage:** Continuously monitors the air quality to detect any chemical changes that could indicate combustion.

2. **SHT31 Sensor for Humidity Measurement**
   - **Type:** Humidity sensor
   - **Purpose:** Measures the relative humidity of the environment. A sudden drop in humidity can be an indicator of a fire nearby.
   - **Usage:** Data from this sensor is used to assess environmental conditions and validate other fire indicators.

3. **BME280 Sensor for Pressure Measurement**
   - **Type:** Atmospheric pressure sensor
   - **Purpose:** Measures atmospheric pressure. Significant changes in pressure can be related to weather conditions or thermal updrafts from a fire.
   - **Usage:** Helps in understanding the meteorological conditions and assessing potential fire behavior.

### Machine Learning Models

1. **Random Forest Classification**
   - **Purpose:** Predicts the likelihood of a fire based on sensor data (TVOC, eCO2, humidity, and pressure). This model analyzes patterns and trends in the sensor data to make informed predictions about potential fire events.
   - **Implementation:** The model is trained with historical sensor data labeled with fire occurrence information, learning to distinguish normal conditions from those likely to indicate a fire.

2. **Convolutional Neural Networks (CNN)**
   - **Purpose:** Analyzes images to detect visual signs of fire. This model is capable of recognizing smoke, flames, and other visual indicators of fire in images.
   - **Implementation:** Trained on a dataset of images labeled as 'fire' and 'no fire', the CNN model learns features associated with fires, enhancing the system’s ability to detect fires through visual monitoring.

## Setup and Installation

- Ensure that all sensors are connected properly to your microcontroller or data acquisition system.
- Install the necessary libraries for interfacing with the SGP30, SHT31, and BME280 sensors. Common libraries are available for platforms like Arduino and Raspberry Pi.
- Set up your environment for running Python, with packages such as `sklearn` for Random Forest models and `tensorflow` or `keras` for CNN models.
- Deploy the sensor network in a strategic location to ensure optimal coverage and data accuracy.

## Usage

1. Start by calibrating each sensor according to the manufacturer's instructions to ensure accurate readings.
2. Collect data continuously from the sensors and feed this into the Random Forest model to evaluate the likelihood of fire.
3. Simultaneously, capture images from cameras in the area to be analyzed by the CNN model for visual signs of fire.
4. Integrate alerts and notifications to inform relevant personnel or authorities when a fire is detected or predicted by the models.

For more detailed information on the configuration and technical specifications, please refer to the individual sensor datasheets and machine learning model documentation.

## Contributing

Contributions to the Flare Watcher project are welcome. This can include enhancing the machine learning models, improving sensor integration, or expanding the system's capabilities. Please submit pull requests or issue reports through this repository.

## License

This project is licensed under [license name]. See the LICENSE file for more details.

