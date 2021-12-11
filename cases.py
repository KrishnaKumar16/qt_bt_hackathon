from driver_utilities import DriverUtilities
from mobile_actions import MobileActions
from logs import Logs
from locator_strategies import androidLocator, xpath


def case1():
    DriverUtilities.start_appium_server()
    ue1_driver = DriverUtilities.create_driver_for_ue1()
    ue2_driver = DriverUtilities.create_driver_for_ue2()
    ue1 = MobileActions(ue1_driver)
    ue2 = MobileActions(ue2_driver)
    ue2_phone_number = ue2.fetch_mobile_number()
    ue1.makePhoneCall(ue2_phone_number)
    ue2.sleepFor(4)
    ue2.accept_phone_call()
    ue2.sleepFor(42)
    ue2.disconnect_the_call()
    DriverUtilities.kill_appium_server()

def case2():
    DriverUtilities.start_appium_server()
    ue1_driver = DriverUtilities.create_driver_for_ue1()
    ue2_driver = DriverUtilities.create_driver_for_ue2()
    ue1 = MobileActions(ue1_driver)
    ue2 = MobileActions(ue2_driver)
    ue2_phone_number = ue2.fetch_mobile_number()
    ue1.send_sms(phone_number=ue2_phone_number, sms_content='India Won the paytm t20 series')
    DriverUtilities.kill_appium_server()

def case3():
    download_file_size = 1000
    expected_download_amount = 500
    # DriverUtilities.start_appium_server()
    ue1_driver = DriverUtilities.create_driver_for_ue1()
    ue1 = MobileActions(ue1_driver)
    ue1.launch_chrome()
    chrome_url = androidLocator(xpath("//*[@resource-id='com.android.chrome:id/url_bar'] | //*[@resource-id='com.android.chrome:id/search_box_text']"))
    #Clear url
    ue1.element(chrome_url).clear_text()
    ue1.element(chrome_url).click()
    #To download 1gb file
    ue1.element(chrome_url).click()
    ue1.element(chrome_url).fill_text(f"http://testfiles.hostnetworks.com.au/{download_file_size}MB.iso")
    ue1.press_enter()
    download_button = androidLocator(xpath("//*[@text='Download']"))
    if ue1.element(download_button).isElementPresent(3):
        ue1.element(download_button).click()
    more_options_icon = androidLocator(xpath("//*[@resource-id='com.android.chrome:id/menu_badge'] | //*[@resource-id='com.android.chrome:id/menu_button']"))
    ue1.element(more_options_icon).click()
    downloads_option = androidLocator(xpath("//*[@text='Downloads']"))
    ue1.element(downloads_option).click()
    download_amount_status = androidLocator(xpath("(//*[contains(@text, 'left')])[1]"))
    ue1.element(download_amount_status).waitUntilElementIsPresent(wait=2)
    download_status_element = ue1.element(download_amount_status).elementNativeAction(wait=0)

    def is_500mb_downloaded():
        d_status = str(download_status_element.text)
        download_amount = int(d_status.split('MB')[0].strip().split('.')[0])
        Logs.log_info(f"{download_amount}MB has been downloaded")
        if download_amount >= expected_download_amount:
            Logs.log_info(f"Reached the expected amount of file size - {expected_download_amount}")
            return True
        else:
            return False
    pause_button = androidLocator(xpath("//*[contains(@text, 'left')]/preceding-sibling::android.widget.ImageButton"))
    pause_button_element = ue1.element(pause_button).elementNativeAction(wait=0)
    while is_500mb_downloaded() is False:
        continue
    pause_button_element.click()
    ue1.terminate_chrome()
    # DriverUtilities.kill_appium_server()

Logs()
case3()
