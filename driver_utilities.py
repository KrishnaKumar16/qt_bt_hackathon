from appium import webdriver
import subprocess
from appium.webdriver.appium_service import AppiumService
from logs import Logs
import os
from datetime import datetime


class DriverUtilities:
    __appium_server: AppiumService = None

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
    def start_appium_server():
        host = '127.0.0.1'
        port_number = '4726'
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
        appium_log_file = str(os.path.join(DriverUtilities.get_root_directory(), 'appium_logs.txt')).replace('\\', '/')
        DriverUtilities.delete_file_if_present(appium_log_file)
        Logs.log_info(f"Starting appium server in port - {port_number}")
        DriverUtilities.__appium_server = AppiumService()
        DriverUtilities.__appium_server.start(
            args=['--address', host, '-p', port_number, '--relaxed-security', f'--log="{appium_log_file}"'],
            timeout_ms=10000,
            main_script=f"{appium_path}/node_modules/appium/build/lib/main.js"
        )
        assert DriverUtilities.__appium_server.is_running is True
        assert DriverUtilities.__appium_server.is_listening is True

    @staticmethod
    def kill_appium_server():
        Logs.log_info("Stopping the appium server")
        DriverUtilities.__appium_server.stop()

    @staticmethod
    def delete_file_if_present(file_path):
        file_path = os.path.join(file_path)
        if os.path.isfile(file_path):
            Logs.log_info(f"Deleting file using the path - '{file_path}'")
            os.remove(file_path)
        else:
            Logs.log_info(f"'{file_path}' is not present")

    @staticmethod
    def get_time_stamp():
        return str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

    @staticmethod
    def get_root_directory():
        return str(os.path.dirname(os.path.abspath(__file__)))

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
