from appium import webdriver
import subprocess
import os
from logs import Logs
from time import sleep


class DriverUtilities:

    @staticmethod
    def check_if_appium_is_present_in_path():
        paths = os.environ.get('PATH').split(';')
        for path in paths:
            if path != ' ' or path != '':
                try:
                    for file in os.listdir(path):
                        if 'appium' in file:
                            return path
                except:
                    continue

    @staticmethod
    def start_appium_server(port_number: int = 4726):
        # Kill appium before start
        try:
            subprocess.Popen(f"TASKKILL /F /IM node.exe", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        except:
            pass
        appium_path = DriverUtilities.check_if_appium_is_present_in_path()
        if '\\' in appium_path:
            appium_path = appium_path.replace('\\', '/')
        if appium_path is None:
            Logs.log_error("appium is not installed on the PC, "
                           "if it is installed please add it to "
                           "the environment variable or use 'npm install -g appium' to install it")
            raise Exception("appium is not installed on the PC, "
                            "if it is installed please add it to "
                            "the environment variable or use 'npm install -g appium' to install it")
        command = f'"{appium_path}/appium" -p {port_number} --relaxed-security'
        # Logs.log_info(f"Starting appium server in port - {port_number}")
        process = subprocess.Popen(command, cwd=appium_path,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        out, err = process.communicate()
        out = out.decode('utf-8').split('\n')
        for line in out:
            if 'http interface listener started on' in line:
                Logs.log_info(out)
        # sleep(8)
        return process

    @staticmethod
    def create_driver_for_ue1(udid: str = None):
        if udid is None:
            caps = dict(platformName='Android', udid=str(DriverUtilities.get_udid_of_devices()[0]))
        else:
            caps = dict(platformName='Android', udid=udid)
        return DriverUtilities.get_driver(url="http://127.0.0.1:4726/wd/hub", desired_capabilities=caps)

    @staticmethod
    def create_driver_for_ue2(udid: str = None):
        if udid is None:
            udids = DriverUtilities.get_udid_of_devices()
            if len(udids) == 0:
                Logs.log_error("There are no devices connected to the PC")
                raise Exception("There are no devices connected to the PC")
            elif len(udids) == 1:
                Logs.log_error("There is only one device connected to the PC")
                raise Exception("There is only one device connected to the PC")
            caps = dict(platformName='Android', udid=str(DriverUtilities.get_udid_of_devices()[1]))
        else:
            caps = dict(platformName='Android', udid=udid)
        return DriverUtilities.get_driver(url="http://127.0.0.1:4726/wd/hub", desired_capabilities=caps)

    @staticmethod
    def get_driver(url, desired_capabilities):
        return webdriver.Remote(command_executor=url, desired_capabilities=desired_capabilities)

    @staticmethod
    def get_udid_of_devices():
        process = subprocess.Popen("adb devices", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        result = [item.replace('\r', '') for item in out.decode('utf-8').split('\n')]
        result = [item for item in result if item != '']
        result.remove('List of devices attached')
        udid = []
        for item in result:
            if 'device' in item or 'online' in item:
                udid.append(item.split('\t')[0])
        return udid
