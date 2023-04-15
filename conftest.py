from appium import webdriver
import subprocess
import pytest

def get_connected_devices():
    try:
        output = subprocess.check_output(['adb', 'devices'])
        devices = output.decode().strip().split('\n')
        devices = [device.split('\t')[0] for device in devices if 'device' in device]
        return devices
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_device_udid():
    devices = get_connected_devices()
    if len(devices) > 0:
        return devices[0]
    else:
        print("No connected devices found.")
        return None


@pytest.fixture
def driver():
    desired_caps = {
        'autoGrantPermissions': True,
        'deviceName': 'Pixel_5',
        'platformName': 'Android',
        'version': '13.0',
        'udid': 'emulator-5554',
        'appPackage': 'com.ajaxsystems',
        'appActivity': 'com.ajaxsystems.ui.activity.LauncherActivity'

    }
    return webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
