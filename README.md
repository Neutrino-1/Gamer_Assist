# Gamer Assist

A python application to capture the onscreen health data of a game to process onscreen health and send it to 
hardware device through serial communication.

Python Application Feature :
* Saving different games health bar location / processing information
* Interactive screenshot to get the healthbar / health value co-ordinates
* Customizable serial communication (ports / badu rate selection)
* In built image editor
* Performs OCR on Health value
* Determines Health value based on Health bar

![Gamer Assist](https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/Game%20gif.gif)

Arduino Application Feautre:
* ESP-NOW integrated
* Reads data from serial  
* Drive different addressable RGB leds

#### Ambient Light Circuit
<img src="https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/Ambient%20light%20system.png" width="50%" height="50%">

#### Haptic feedback Circuit
<img src="https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/Haptic%20feedback.png" width="50%" height="50%">

### Getting Started

#### Prerequisites

* [Python 3](https://www.python.org/downloads/)
* [Arduino IDE](https://arduino.cc/)
* [Tessract](https://github.com/tesseract-ocr/tesseract) 


### Python Application

#### Python External Library Prerequisites

* Open CV
* Pillow
* numpy
* pyserial
* pytesseract
* pyautogui

#### Runnig the code 

Navigate to the main.py file location and run the command in cmd/power shell.

```
Python main.py 
```
#### Usage

Home page - Here select the com port where the device is connected and set the badu rate.

![Home window](https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/Home.PNG)

Interactive Screenshot - select the part of the screen where the health bar or health value is located.
(Make sure the image/game is full screen when you do this)

Selection of health bar
<br/>
<img src="https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/Interactive%20screenshot%20health%20bar.png" width="50%" height="50%">

Selection of health value
<br/>
<img src="https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/Interactive%20screenshot%20health%20value.png" width="50%" height="50%">

Editor Window - Here the images are processed to get the health value by using sliders (threshold, brightness and blur).

Editing for health bar
<br/>
![Health bar editor](https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/editor%20for%20health%20bar.PNG)

Editing for health value
<br/>
![Helath value editor](https://github.com/Neutrino-1/Gamer_Assist/blob/master/readme_img/health%20value.PNG)

### Arduino

#### Arduino External Library Prerequisites
* [ESP-Core](https://github.com/esp8266/Arduino) - by Ivan Grokhotkov
* [NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel) - by Adafruit
* [Fast LED](https://github.com/FastLED/FastLED)

Open the Arduino IDE and follow the below steps:
```
Sketch -> include library -> ManageLibrary -> *Search for the above libraries*
```
Or
follow the instructions on respective library repository.

Video explanation for hardware/circuit: [Youtube link](https://www.youtube.com/watch?v=Fs9OwsaYeDM)

## BUGS
This is the first version so there are way to many bugs for now, let me know what issues you find.
The latency of processing the health value varies dpending on the specs of the PC. 

## License 
[LICENSE.md](https://github.com/Neutrino-1/Gamer_Assist/blob/master/LICENSE.md) file for details

