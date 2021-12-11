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

def case2():
    server = DriverUtilities.start_appium_server()
    ue1_driver = DriverUtilities.create_driver_for_ue1()
    ue2_driver = DriverUtilities.create_driver_for_ue2()
    ue1 = MobileActions(ue1_driver)
    ue2 = MobileActions(ue2_driver)
    ue2_phone_number = ue2.fetch_mobile_number()
    ue1.send_sms(phone_number=ue2_phone_number, sms_content='India Won the paytm t20 series')
    server.terminate()

def case3():
    server = DriverUtilities.start_appium_server()

    ue1_driver = DriverUtilities.create_driver_for_ue1()
    ue1 = MobileActions(ue1_driver)
    ue1.launch_chrome()
    chrome_url = androidLocator(xpath("//*[@resource-id='com.android.chrome:id/url_bar'] | //*[@resource-id='com.android.chrome:id/search_box_text']"))
    #Clear url
    ue1.element(chrome_url).clear_text()
    ue1.element(chrome_url).click()
    #To download 1gb file
    ue1.element(chrome_url).click()
    ue1.element(chrome_url).fill_text("http://testfiles.hostnetworks.com.au/1000MB.iso")
    ue1.press_enter()
    download_button = androidLocator(xpath("//*[@text='Download']"))
    if ue1.element(download_button).isElementPresent(3):
        ue1.element(download_button).click()
    more_options_icon = androidLocator(xpath("//*[@resource-id='com.android.chrome:id/menu_badge'] | //*[@resource-id='com.android.chrome:id/menu_button']"))
    ue1.element(more_options_icon).click()
    downloads_option = androidLocator(xpath("//*[@text='Downloads']"))
    ue1.element(downloads_option).click()
    def is_500mb_downloaded():
        download_amount_status = androidLocator(xpath("(//*[contains(@text, '/ 1.00 GB')])[1]"))
        d_status = str(ue1.element(download_amount_status).get_text())
        download_amount = int(d_status.split('MB')[0].strip().split('.')[0])
        if download_amount >= 500:
            return True
        else:
            return False
    pause_button = androidLocator(xpath("//android.widget.ImageButton[@content-desc='Pause']"))
    while is_500mb_downloaded() is False:
        continue
    else:
        ue1.element(pause_button).click()
    ue1.sleepFor(5)
    server.terminate()

Logs()
case3()