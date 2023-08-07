# TwitchWatcher

- Simple automated tool for watching Twitch streames and collectings drops/chat bonusses
- Using selenium-chrome python avoiding Twitch API
- Built especially for running on Raspberry Pi4.

## Dependencies

- Works on Linux and Windows, x86 and ARM
- Python 3.11 is required
- Uses selenium, undetected_chromedriver, keyboard and platform
- Webdriver for chrome needs to be put in driver dir

## How to RPi4 (ARM)
- Tested on RPi4 running Ubuntu Server (ARM64)
- On arm there's no Chrome support, so workaround with Chromium has to be done
- Update
 'sudo apt-get update && sudo apt-get upgrade'
- Clone this repository with 
 'git clone https://github.com/kubikulek231/TwitchWatcher/'
- Install python3.11 and pip
 'sudo apt-get install python3.11'
 'sudo apt-get install pip3'
- Now install Chromium browser
 'sudo apt-get install chromium-browser'
 'sudo pip3 install selenium'
 'sudo pip3 install undetected-chromedriver'
 'sudo pip3 install keyboard'
 'sudo pip3 install platform'
- Now install Chromium Webdriver (no need to put 
 'sudo apt-get install chromium-webdriver'
- Run 'sudo python3 main.py' and you should be done