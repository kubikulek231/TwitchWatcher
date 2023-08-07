#!/usr/bin/python
import io
import os
import random
import re
import string
import platform

driver_name = 'chromedriver'


@staticmethod
def is_rpi4():
    return platform.machine() == 'aarch64'


def get_webdriver_name(driver_file_name: str = "chromedriver") -> bool:
    if os.name == "nt":  # Windows
        driver_path = f"{driver_file_name}.exe"
    else:  # Assuming other OS (Linux, macOS, etc.)
        driver_path = f"{driver_file_name}"
    if is_rpi4():
        driver_path = '/usr/lib/chromium-browser/chromedriver'
    return driver_path


def random_cdc():
    cdc = random.choices(string.ascii_lowercase, k=26)
    cdc[-6:-4] = map(str.upper, cdc[-6:-4])
    cdc[2] = cdc[0]
    cdc[3] = "_"
    return "".join(cdc).encode()


def patch_binary():
    """
    Patches the ChromeDriver binary
    :return: False on failure, binary name on success
    """
    linect = 0
    replacement = random_cdc()
    with io.open(get_webdriver_name(driver_name), "r+b") as fh:
        for line in iter(lambda: fh.readline(), b""):
            if b"cdc_" in line:
                fh.seek(-len(line), 1)
                newline = re.sub(b"cdc_.{22}", replacement, line)
                fh.write(newline)
                linect += 1
        return linect


if __name__ == '__main__':
    try:
        patch_binary()
        print("success")
    except Exception as e:
        print("not successful")
        print(e)
    input("press a key to exit")
