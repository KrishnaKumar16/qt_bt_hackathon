from selenium.common.exceptions import InvalidSessionIdException, SessionNotCreatedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from appium.webdriver.webdriver import MobileWebElement, WebDriver as MobileDriver
from datetime import datetime
from unittest.case import TestCase
from time import sleep
from appium.webdriver.common.multi_action import MultiAction
import base64
from appium.webdriver.common.touch_action import TouchAction
from logs import Logs
from locator_strategies import androidLocator, xpath
from driver_utilities import DriverUtilities


class MobileActions:
    __MobileLocator = dict(android=Tuple[str, str], ios=Tuple[str, str])
    __DEFAULT_WAIT_TIME = 10

    def __init__(self, mobileDriver: MobileDriver):
        self.__driver = mobileDriver

    def getCurrentAppPackageOfAndroidOrBudleIDOfIOS(self):
        if self.check_if_current_platform_is_android() is True:
            return str(self.__driver.desired_capabilities['desired']['appPackage'])
        elif self.checkIfCurrentPlatformIsIOS() is True:
            return str(self.__driver.desired_capabilities['desired']['bundleId'])

    def check_if_current_platform_is_android(self):
        if self.getPlatformFromCapablities() == 'android':
            return True
        else:
            return False

    def checkIfCurrentPlatformIsIOS(self):
        if self.getPlatformFromCapablities() == 'ios':
            return True
        else:
            return False

    def getPlatformFromCapablities(self):
        return str(self.__driver.desired_capabilities['desired']['platformName']).lower().strip()

    def activate_app(self, bundleIdOfIosOrAppPackageOfAndroid):
        self.__driver.activate_app(bundleIdOfIosOrAppPackageOfAndroid)
        return self

    def getWindowSize(self):
        return self.__driver.get_window_size()['width'], self.__driver.get_window_size()['height']

    def scrollDown(self, scrollFromCenterOfTheScreen: bool = True):
        width, height = self.__driver.get_window_size()
        if scrollFromCenterOfTheScreen is False:
            width = 0
        TouchAction(self.__driver).press(width * 0.5, height * 0.7) \
            .wait(ms=2000).move_to(width * 0.5, height * 0.2).release().perform()
        return self

    def scrollUp(self, scrollFromCenterOfTheScreen: bool = True):
        width, height = self.__driver.get_window_size()
        if scrollFromCenterOfTheScreen is False:
            width = 0
        TouchAction(self.__driver).press(width * 0.5, height * 0.2) \
            .wait(ms=2000).move_to(width * 0.5, height * 0.7).release().perform()
        return self

    def installApp(self, appPath, grantPermissions: bool = True,
                   replace: bool = True,
                   timeoutInMicroSeconds: int = 60000,
                   allowTestPackages: bool = False,
                   useSdcard: bool = False):

        self.__driver.install_app(app_path=appPath, grantPermissions=grantPermissions,
                                  replace=replace,
                                  timeout=timeoutInMicroSeconds,
                                  allowTestPackages=allowTestPackages,
                                  useSdcard=useSdcard)
        return self

    def putTheAppInBackground(self, seconds: int = None):
        self.__driver.background_app(seconds)
        return self

    def closeApp(self):
        self.__driver.close_app()
        return self

    def launchApp(self):
        self.__driver.launch_app()
        return self

    def isAppAlreadyInstalled(self, bundleIdOfIosOrAppPackageOfAndroid):
        return self.__driver.is_app_installed(bundleIdOfIosOrAppPackageOfAndroid)

    def sleepFor(self, seconds: int):
        sleep(seconds)
        return self

    def unInstallApp(self, bundleIdOfIosOrAppPackageOfAndroid):
        self.__driver.remove_app(bundleIdOfIosOrAppPackageOfAndroid)
        return self

    def uninstallAppIfItIsPresent(self, bundleIdOfIosOrAppPackageOfAndroid):
        if self.isAppAlreadyInstalled(bundleIdOfIosOrAppPackageOfAndroid) is True:
            self.unInstallApp(bundleIdOfIosOrAppPackageOfAndroid)
        return self

    def reInstallApp(self, appPath, bundleIdOfIosOrAppPackageOfAndroid):
        if self.isAppAlreadyInstalled(bundleIdOfIosOrAppPackageOfAndroid) is True:
            self.unInstallApp(bundleIdOfIosOrAppPackageOfAndroid)
            self.installApp(appPath)
        else:
            self.installApp(appPath)
        return self

    def lockDevice(self):
        self.__driver.lock()
        return self

    def unlockDevice(self):
        self.__driver.unlock()
        return self

    def resetApp(self):
        self.__driver.reset()
        return self

    def __getTimeStamp(self):
        return str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

    def getTouchActions(self):
        return TouchAction(self.__driver)

    def clickUsingCoOrdinates(self, x: int, y: int, numberOfClicks: int = None):
        self.getTouchActions().tap(x=x, y=y, count=numberOfClicks).perform()
        return self

    def startScreenRecording(self):
        self.__driver.start_recording_screen()
        return self

    def stopScreenRecording(self, destinationFolderPath):
        base64Video = self.__driver.stop_recording_screen()
        with open(destinationFolderPath + '/' + self.__getTimeStamp() + '.mp4', 'wb') as video:
            video.write(base64.b64decode(base64Video))
        return self

    def getMultiTouchAction(self):
        return MultiAction(self.__driver)

    def element(self, mobileLocator: __MobileLocator):
        return self.__MobileActionDefinitions(self.__driver, mobileLocator)

    def captureScreenshot(self, destinationFolderPath):
        self.__driver.get_screenshot_as_file(destinationFolderPath + self.__getTimeStamp() + '.png')
        return self

    def getScreenShotAsBase64(self):
        return self.__driver.get_screenshot_as_base64()

    def execute_script(self, command, *args):
        return self.__driver.execute_script('mobile:shell', {"command": command, "args": args})

    def makePhoneCall(self, phone_number):
        if self.check_if_current_platform_is_android():
            Logs.log_info(f'Making a phone call to {phone_number}')
            self.execute_script('am', f"start -a android.intent.action.CALL -d tel:{phone_number}")
            self.sleepFor(2)
            if self.element(androidLocator(xpath("//*[contains(@resource-id,'disconnect') and contains(@class, 'Button')] | //*[@id='com.samsung.android.incallui:id/disconnect_button'] | //*[@resource-id='com.samsung.android.incallui:id/disconnect_button']"))).isElementPresent(3) is False:
                self.execute_script("input keyevent 5")
        else:
            raise Exception("'make_phone_call' method is not implemented for iOS")
    
    def get_current_server_url(self):
        """To fetch current appium server url"""
        return self.__driver.command_executor._url

    def is_driver_corrupted(self):
        """To check whether current driver is corrupted"""
        try:
            self.__driver.get_screenshot_as_png()
            return False
        except InvalidSessionIdException:
            Logs.log_info("Mobile driver is corrupted")
            return True
        except SessionNotCreatedException:
            return True


    def get_current_capabilities(self):
        """
        To fetch current capabilities
        :return: platform name
        """
        Logs.log_info("Fetching current capabilities")
        return self.__driver.desired_capabilities

    def relaunch_driver(self):
        """To relaunch driver"""
        caps = self.get_current_capabilities()
        copy_caps = caps.copy()
        app_related_caps = {}
        if 'app' in caps.keys():
            app_related_caps['app'] = copy_caps['app']
            copy_caps.pop('app')
        if 'otherApps' in caps.keys():
            app_related_caps['otherApps'] = copy_caps['otherApps']
            copy_caps.pop('otherApps')
        Logs.log_info("Relaunching the driver")
        return DriverUtilities.get_driver(url=self.get_current_server_url(), desired_capabilities=copy_caps)

    def fetch_mobile_number(self):
        """To fetch mobile number from the current device"""
        result = str(self.execute_script("service call iphonesubinfo 15 | cut -c 52-66 | tr -d '.[:space:]' && echo")).strip()
        length_of_result = len(result)
        Logs.log_info("Trying to fetch the mobile number")
        Logs.log_info(f"The fetched value is '{result}'")
        if result.isdigit():
            if length_of_result == 10 or length_of_result == 11 or length_of_result == 9:
                return result
            else:
                raise Exception(f"Fetched value is - '{result}', and it does not pass the phone number constraints")
        else:
            raise Exception(f"Fetched value is - '{result}', and it does not pass the phone number constraints")

    def accept_phone_call(self):
        """
        To accept the incoming phone call, this method is compatible for android devices only.
        """
        Logs.log_info(f'Accepting the phone call')
        self.execute_script("input keyevent 5")

    def disconnect_the_call(self):
        Logs.log_info(f'Disconnecting the phone call')
        call_end_button = androidLocator(xpath("//*[contains(@resource-id,'disconnect') and contains(@class, 'Button')] | //*[@id='com.samsung.android.incallui:id/disconnect_button'] | //*[@resource-id='com.samsung.android.incallui:id/disconnect_button']"))
        self.element(call_end_button).click()

    def send_sms(self, phone_number, sms_content):
        Logs.log_info(f'Sending sms to "{phone_number}" with the content "{sms_content}"')
        adb_command = f'adb shell service call isms 7 i32 0 s16 "com.android.mms.service" s16 "{phone_number}" s16 "null" s16 "{sms_content}" s16 "null" s16 "null"'

    def is_phone_ringing(self):
        """To check if phone is ringing"""
        result = str(self.execute_script("dumpsys telephony.registry | grep mCallState")).split()[0].replace('mCallState=', '').strip()
        if result == '1':
            return True
        else:
            return False

    def is_phone_not_ringing(self):
        """To check if phone is not ringing"""
        # result = str(self.execute_script("dumpsys telephony.registry | grep mCallState")).replace('mCallState=', '').strip()
        result = str(self.execute_script("dumpsys telephony.registry | grep mCallState")).split()[0].replace(
            'mCallState=', '').strip()
        if result == '0':
            return True
        else:
            return False

    def is_there_any_ongoing_call(self):
        """To check if there is any ongoing call"""
        # result = str(self.execute_script("dumpsys telephony.registry | grep mCallState")).replace('mCallState=', '').strip()
        result = str(self.execute_script("dumpsys telephony.registry | grep mCallState")).split()[0].replace(
            'mCallState=', '').strip()
        result = result.replace('mCallState=', '').strip()
        if result == '2':
            return True
        else:
            return False
        
    def launch_chrome(self):
        """
        To launch chrome browser
        """
        if self.check_if_current_platform_is_android():
            Logs.log_info('Launching chrome browser')
            self.activate_app('com.android.chrome')
        else:
            raise Exception("'launch_chrome' method is not implemented for iOS")

    def press_enter(self):
        """
        To press enter key in android
        """
        if self.check_if_current_platform_is_android():
            Logs.log_info("Pressing enter key")
            self.__driver.press_keycode(66)
        else:
            raise Exception("'go_to_home_screen' method is not implemented for iOS")

    class __MobileActionDefinitions:
        __MobileLocator = dict(android=Tuple[str, str], ios=Tuple[str, str])
        __DEFAULT_WAIT_TIME = 10

        def __init__(self, driver: MobileDriver, locator: __MobileLocator):
            self.locator = locator
            self.__driver = driver
            self.__locator = self.getPlatformBasedLocator()

        def getTestUtils(self):
            return TestCase()

        def __getTimeStamp(self):
            return str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

        def getTouchActions(self):
            return TouchAction(self.__driver)

        def getMultiTouchAction(self):
            return MultiAction(self.__driver)

        def clickUsingCoOrdinates(self, x: int, y: int, numberOfClicks: int = None):
            self.getTouchActions().tap(x=x, y=y, count=numberOfClicks)
            return self

        def activate_app(self, bundleIdOfIosOrAppPackageOfAndroid):
            self.__driver.activate_app(bundleIdOfIosOrAppPackageOfAndroid)
            return self

        def putTheAppInBackground(self, seconds: int = None):
            self.__driver.background_app(seconds)
            return self

        def click(self, wait: int = __DEFAULT_WAIT_TIME):
            Logs.log_info(f"Performing click on element with path {self.__locator}")
            self.elementNativeAction(wait).click()
            return self

        def fill_text(self, text, wait: int = __DEFAULT_WAIT_TIME):
            Logs.log_info(f"Entering text in element with path {self.__locator}")
            self.elementNativeAction(wait).send_keys(text)
            return self

        def clear_text(self, wait: int = __DEFAULT_WAIT_TIME):
            Logs.log_info(f"Clearing text in element with path {self.__locator}")
            self.elementNativeAction(wait).clear()
            return self

        def sleepFor(self, seconds: int):
            sleep(seconds)
            return self

        def getPlatformFromCapablities(self):
            return str(self.__driver.desired_capabilities['desired']['platformName']).lower().strip()

        def check_if_current_platform_is_android(self):
            if self.getPlatformFromCapablities() == 'android':
                return True
            else:
                return False

        def checkIfCurrentPlatformIsIOS(self):
            if self.getPlatformFromCapablities() == 'ios':
                return True
            else:
                return False

        def getPlatformBasedLocator(self):
            if self.check_if_current_platform_is_android() is True:
                return self.locator['android']
            elif self.checkIfCurrentPlatformIsIOS() is True:
                return self.locator['ios']

        def elementNativeAction(self, wait=__DEFAULT_WAIT_TIME):
            try:
                self.waitUntilElementIsPresent(wait)
            except:
                pass
            element: MobileWebElement = self.__driver.find_element(self.__locator[0], self.__locator[1])
            return element

        def elementsNativeAction(self, wait=__DEFAULT_WAIT_TIME):
            try:
                self.waitUntilElementsArePresent(wait)
            except:
                pass
            return self.__driver.find_elements(self.__locator[0], self.__locator[1])

        def getWindowSize(self):
            return self.__driver.get_window_size()['width'], self.__driver.get_window_size()['height']

        def swipeUsingCoOrdinates(self, startCoOrdinates: Tuple[int, int],
                                  endCoOrdinates: Tuple[int, int]):
            TouchAction(self.__driver).press(x=int(startCoOrdinates[0]), y=int(startCoOrdinates[1])) \
                .wait(ms=2000).move_to(x=int(endCoOrdinates[0]), y=int(endCoOrdinates[1])) \
                .release().perform()
            return self

        def scrollDown(self, scrollFromCenterOfTheScreen: bool = True, xCordinate: int = None,
                       yCoOrdinateStartingPoint: int = None):
            width, height = self.getWindowSize()
            width, height = float(width), float(height)
            if scrollFromCenterOfTheScreen is False:
                width = 0
            if xCordinate is None and yCoOrdinateStartingPoint is None:
                self.swipeUsingCoOrdinates(startCoOrdinates=(int(width * 0.5), int(height * 0.7)),
                                           endCoOrdinates=(int(width * 0.5), int(height * 0.2)))
            elif yCoOrdinateStartingPoint is None and xCordinate is not None:
                self.swipeUsingCoOrdinates(startCoOrdinates=(xCordinate, int(height * 0.7)),
                                           endCoOrdinates=(xCordinate, int(height * 0.2)))
            elif yCoOrdinateStartingPoint is not None and xCordinate is None:
                self.swipeUsingCoOrdinates(startCoOrdinates=(int(width * 0.5), yCoOrdinateStartingPoint),
                                           endCoOrdinates=(int(width * 0.5), int(height * 0.2)))
            else:
                self.swipeUsingCoOrdinates(startCoOrdinates=(xCordinate, yCoOrdinateStartingPoint),
                                           endCoOrdinates=(xCordinate, int(height * 0.2)))
            return self

        def scrollUp(self, scrollFromCenterOfTheScreen: bool = True, xCordinate: int = None,
                     yCoOrdinateStartingPoint: int = None):
            width, height = self.getWindowSize()
            width, height = float(width), float(height)
            if scrollFromCenterOfTheScreen is False:
                width = 0
            if xCordinate is None and yCoOrdinateStartingPoint is None:
                self.swipeUsingCoOrdinates(startCoOrdinates=(int(width * 0.5), int(height * 0.2)),
                                           endCoOrdinates=(int(width * 0.5), int(height * 0.7)))
            elif yCoOrdinateStartingPoint is None and xCordinate is not None:
                self.swipeUsingCoOrdinates(startCoOrdinates=(xCordinate, int(height * 0.2)),
                                           endCoOrdinates=(xCordinate, int(height * 0.7)))
            elif yCoOrdinateStartingPoint is not None and xCordinate is None:
                self.swipeUsingCoOrdinates(startCoOrdinates=(int(width * 0.5), yCoOrdinateStartingPoint),
                                           endCoOrdinates=(int(width * 0.5), int(height * 0.7)))
            else:
                self.swipeUsingCoOrdinates(startCoOrdinates=(xCordinate, yCoOrdinateStartingPoint),
                                           endCoOrdinates=(xCordinate, int(height * 0.7)))
            return self

        def scrollDownUntilElementIsFound(self, wait: int = 2, maximumScrolls: int = 10,
                                          scrollFromCenterOfTheScreen: bool = True, xCordinate: int = None,
                                          yCoOrdinateStartingPoint: int = None):
            count = 0
            while self.isElementDisplayed(wait) is False and count <= maximumScrolls:
                count += 1
                self.scrollDown(scrollFromCenterOfTheScreen, xCordinate, yCoOrdinateStartingPoint)
                if self.isElementDisplayed(wait) is True:
                    break
                else:
                    continue
            if self.isElementDisplayed(wait=0) is False and count >= maximumScrolls:
                raise Exception('Element is not present even after scrolling down ' + str(count) + ' times')
            return self

        def get_text(self):
            return self.elementNativeAction().text

        def getListOfTextFromElements(self):
            listOfText = []
            for element in self.elementsNativeAction():
                listOfText.append(element.text)
            return listOfText

        def getListOfAttributesFromElements(self, attributeName):
            listOfText = []
            for element in self.elementsNativeAction():
                listOfText.append(element.get_attribute(attributeName))
            return listOfText

        def getAttribute(self, attributeName):
            return self.elementNativeAction().get_attribute(attributeName)

        def validateElementIsPresent(self, wait=__DEFAULT_WAIT_TIME):
            self.getTestUtils().assertTrue(self.isElementPresent(wait), str(self.__locator) + ' is not present')
            return self

        def validateElementIsNotPresent(self, wait=__DEFAULT_WAIT_TIME):
            self.getTestUtils().assertFalse(self.isElementPresent(wait), str(self.__locator) + ' is present')
            return self

        def validateElementIsDisplayed(self, wait=__DEFAULT_WAIT_TIME):
            self.getTestUtils().assertTrue(self.isElementDisplayed(wait), str(self.__locator) + ' is not present')
            return self

        def validateElementIsNotDisplayed(self, wait=__DEFAULT_WAIT_TIME):
            self.getTestUtils().assertFalse(self.isElementDisplayed(wait), str(self.__locator) + ' is present')
            return self

        def validateElementsArePresent(self, wait=__DEFAULT_WAIT_TIME):
            self.getTestUtils().assertTrue(self.areElementsPresent(wait), str(self.__locator) + ' is not present')
            return self

        def validateElementsAreNotPresent(self, wait=__DEFAULT_WAIT_TIME):
            self.getTestUtils().assertFalse(self.areElementsPresent(wait), str(self.__locator) + ' is present')
            return self

        def validateListOfElementsContainsText(self, expectedText):
            for elementText in self.getListOfTextFromElements():
                self.getTestUtils().assertIn(elementText, expectedText)
            return self

        def validateListOfElementsNotContainsText(self, expectedText):
            for elementText in self.getListOfTextFromElements():
                self.getTestUtils().assertNotIn(elementText, expectedText)
            return self

        def validateListOfElementsContainsAttribute(self, attributeNme, expectedText):
            for elementText in self.getListOfAttributesFromElements(attributeNme):
                self.getTestUtils().assertIn(elementText, expectedText)
            return self

        def validateListOfElementsNotContainsAttribute(self, attributeNme, expectedText):
            for elementText in self.getListOfAttributesFromElements(attributeNme):
                self.getTestUtils().assertNotIn(elementText, expectedText)
            return self

        def validateTextContains(self, expectedText):
            self.getTestUtils().assertIn(container=self.get_text(), member=expectedText)
            return self

        def validateTextNotContains(self, notExpectedText):
            self.getTestUtils().assertNotIn(container=self.get_text(), member=notExpectedText)
            return self

        def validateTextEquals(self, expectedText):
            self.getTestUtils().assertEqual(self.get_text(), expectedText)
            return self

        def validateAttributeContains(self, attribute, expectedText):
            self.getTestUtils().assertIn(container=self.getAttribute(attribute), member=expectedText)
            return self

        def validateAttributeNotContains(self, attribute, notExpectedText):
            self.getTestUtils().assertNotIn(container=self.getAttribute(attribute), member=notExpectedText)
            return self

        def validateAttributeEquals(self, attribute, expectedText):
            self.getTestUtils().assertEqual(self.getAttribute(attribute), expectedText)
            return self

        def scrollUpUntilElementIsFound(self, wait: int = 2, maximumScrolls: int = 10,
                                        scrollFromCenterOfTheScreen: bool = True, xCordinate: int = None,
                                        yCoOrdinateStartingPoint: int = None):
            count = 0
            while self.isElementDisplayed(wait) is False and count <= maximumScrolls:
                count += 1
                self.scrollUp(scrollFromCenterOfTheScreen, xCordinate, yCoOrdinateStartingPoint)
                if self.isElementDisplayed(wait) is True:
                    break
                else:
                    continue
            if self.isElementDisplayed(wait=0) is False and count >= maximumScrolls:
                raise Exception('Element is not present even after scrolling up ' + str(count) + ' times')
            return self

        def waitUntilElementIsPresent(self, wait=__DEFAULT_WAIT_TIME):
            WebDriverWait(self.__driver, wait).until(EC.presence_of_element_located((self.__locator[0],
                                                                                     self.__locator[1])))
            return self

        def waitUntilElementsArePresent(self, wait=__DEFAULT_WAIT_TIME):
            WebDriverWait(self.__driver, wait).until(EC.presence_of_all_elements_located((self.__locator[0],
                                                                                          self.__locator[1])))
            return self

        def waitUntilElementIsNotDisplayed(self, wait=__DEFAULT_WAIT_TIME):
            WebDriverWait(self.__driver, wait).until(EC.invisibility_of_element_located((self.__locator[0],
                                                                                         self.__locator[1])))
            return self

        def waitUntilElementIsVisible(self, wait=__DEFAULT_WAIT_TIME):
            WebDriverWait(self.__driver, wait).until(EC.visibility_of_element_located((self.__locator[0],
                                                                                       self.__locator[1])))
            return self

        def waitUntilElementIsClickable(self, wait=__DEFAULT_WAIT_TIME):
            WebDriverWait(self.__driver, wait).until(EC.element_to_be_clickable((self.__locator[0],
                                                                                 self.__locator[1])))
            return self

        def isElementDisplayed(self, wait=__DEFAULT_WAIT_TIME):
            if wait != 0:
                self.waitUntilElementIsVisible(wait)
            return self.elementNativeAction().is_displayed()

        def areElementsPresent(self, wait=__DEFAULT_WAIT_TIME):
            if wait != 0:
                self.waitUntilElementsArePresent(wait)
            if self.elementsNativeAction() != []:
                return True
            else:
                return False

        def isElementPresent(self, wait=__DEFAULT_WAIT_TIME):
            if wait == 0:
                try:
                    self.__driver.find_element(self.__locator[0], self.__locator[1])
                    return True
                except:
                    return False
            else:
                try:
                    self.waitUntilElementIsPresent(wait)
                    return True
                except:
                    return False

        def isKeyboardDisplayed(self):
            return self.__driver.is_keyboard_shown()

        def hideKeyboard(self):
            self.__driver.hide_keyboard()
            return self

        def hideKeyboardIfItIsDispayed(self):
            if self.isKeyboardDisplayed() is True:
                self.hideKeyboard()
            return self

        def getLocationOfElement(self):
            return self.elementNativeAction().location['x'], self.elementNativeAction().location['y']

        def getListOfCssValuesFromElements(self, CssPropertyName):
            listOfText = []
            for element in self.elementsNativeAction():
                listOfText.append(element.value_of_css_property(CssPropertyName))
            return listOfText

        def getCssPropertyValue(self, cssProperty):
            return self.elementNativeAction().value_of_css_property(cssProperty)

        def validateListOfElementsContainsCssValue(self, cssProperty, expectedText):
            for elementText in self.getListOfCssValuesFromElements(cssProperty):
                self.getTestUtils().assertIn(elementText, expectedText)
            return self

        def validateListOfElementsNotContainsCssValue(self, cssProperty, expectedText):
            for elementText in self.getListOfCssValuesFromElements(cssProperty):
                self.getTestUtils().assertNotIn(elementText, expectedText)
            return self

        def validateCssPropertyValueContains(self, cssProperty, expectedText):
            self.getTestUtils().assertIn(container=self.getCssPropertyValue(cssProperty), member=expectedText)
            return self

        def validateCssPropertyValueNotContains(self, cssProperty, notExpectedText):
            self.getTestUtils().assertNotIn(container=self.getCssPropertyValue(cssProperty), member=notExpectedText)
            return self

        def validateCssPropertyValueEquals(self, cssProperty, expectedText):
            self.getTestUtils().assertEqual(self.getCssPropertyValue(cssProperty), expectedText)
            return self

        def captureScreenshot(self, destinationFolderPath):
            self.__driver.get_screenshot_as_file(destinationFolderPath + self.__getTimeStamp() + '.png')
            return self

        def getScreenShotAsBase64(self):
            return self.__driver.get_screenshot_as_base64()

        def captureElementScreenshot(self, destinationFolderPath):
            self.elementNativeAction().screenshot(destinationFolderPath + self.__getTimeStamp() + '.png')
            return self

        def getElementScreenshotAsBase64(self):
            return self.elementNativeAction().screenshot_as_base64

