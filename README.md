> ⚠ **TwitchWatcher** is now deprecated. Selenium gets detected easilly. Here is a [Playwright port](https://github.com/kubikulek231/TwitchWatcherPlaywright).

# TwitchWatcher

- Simple automated tool for watching Twitch streames and collectings drops/chat bonusses
- Using selenium-chrome python avoiding Twitch API
- Built especially for running on Raspberry Pi4

## Dependencies

- Works on Linux and Windows, x86 and ARM
- Python 3.11 is required
- Uses selenium, undetected_chromedriver, keyboard and platform
- Webdriver for chrome needs to be put in driver dir

## How to RPi4 (ARM)
- Tested on RPi4 running Ubuntu Server (ARM64)
- On ARM, there's no Chrome support, so a workaround with Chromium has to be done.

**Update and upgrade**
```bash
sudo apt-get update && sudo apt-get upgrade
```
**Clone this repository**
```bash
git clone https://github.com/kubikulek231/TwitchWatcher/
```
**Install python3.11 and pip**
```bash
sudo apt-get install python3.11
sudo apt-get install pip3
```

**Install Chromium browser and dependencies**
```bash
sudo apt-get install chromium-browser
sudo pip3 install selenium
sudo pip3 install undetected-chromedriver
sudo pip3 install keyboard
sudo pip3 install platform
```
**Install Chromium Webdriver**
```bash
sudo apt-get install chromium-webdriver
```

**Run the main script**
```bash
sudo python3 main.py
```
