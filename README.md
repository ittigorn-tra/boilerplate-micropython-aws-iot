# Micropython AWS IoT Boilerplate
A project built for enabling ESP32 with Micropython to connect to AWS Iot Core.

# Getting ready
## Choose your IDE
[Thonny IDE](https://thonny.org/) is highly recommended for beginners. 

## Flashing micropython onto your device
You can download Micropython from [Micropython download page](https://micropython.org/download/) then flash your device with it.

# Setting up for the first time
## Copy or create files and derectories to your device
Please make sure you have copied or created all `.py` files in this project to your device.

## Create and populate necessary files not included in this repo
Please make sure you have created all the files below brefore attempting to run the code.

### Certificate and private key file
Please create a "thing" in AWS IoT Core and download the necessary files below from AWS once the setup is completed.
```
creds/device_cert.pem.crt
creds/private.pem.key
creds/AmazonRootCA1.cer
```
#### About `.cer` file type for `AmazonRootCA1.cer`
This project is setup to use `.cer` type of RootCA certificate file since it's more memory-efficient than the plain-text `.pem` file. The certificate is publicly available and can be downloaded via [Amazon Trust Services's repository](https://www.amazontrust.com/repository/) under "Root CAs" section, click to download the "DER" version of "CN=Amazon Root CA 1,O=Amazon,C=US".

### Secret configs
Please create `secret_configs.py` file.
This file is designed to he excluded from the Git repository for security purposes and some configs are machine-specific.
The correct schema of the file can be found in `secret_configs_template.txt`
#### Why using `.py` file instead of the more common `.env` file to store secrets?
On the ESP32 with MicroPython, it is significantly more common and practical to store secrets in a dedicated .py file that is excluded from your repository.
<br>
<br>
While .env files are the standard for desktop and web development, they are less common in the MicroPython ecosystem because they require additional libraries to parse, which consumes limited memory.
<br>
<br>
The `secret_configs.py` file here has already been added to the `.gitignore` file and will be excluded from Git's tracking.

## Install libraries
Please replace `xxx` placeholders below with real WiFi SSID and password.
```python
import mip
from wlan import Wlan

Wlan(ssid='xxx', pwd='xxx').connect()

mip.install('logging')
```

# Expected behavior
This code will keep checking for any MQTT message on the socket print any message that comes in.

# Testing
Run `demo.py` file. then go to AWS IoT Console and use "MQTT Test Client" to publish a message to the topic you specified in your `secret_configs.py` file.

# Ready to go live?
Any code in `boot.py` and `main.py` file will run automatically after boot up. You can put your code in `main.py` file and reboot your device.
