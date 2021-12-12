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
    mp1 = MessagingProcess(ue1)
    mp2 = MessagingProcess(ue2)
    mp1.launch_messages()
    mp2.launch_messages()
    mp1.send_sms(message='India Won the paytm t20 series', phone_number=ue2_phone_number)
    ue1.sleepFor(1)
    mp1.close_messages()
    mp2.verify_sms_is_displayed('India Won the paytm t20 series')
    mp2.close_messages()
    DriverUtilities.kill_appium_server()

def case3():
    download_file_size = 1000
    expected_download_amount = 500
    DriverUtilities.start_appium_server()
    ue1_driver = DriverUtilities.create_driver_for_ue1()
    ue1 = MobileActions(ue1_driver)
    ue1.launch_chrome()
    chrome_url = androidLocator(xpath(
        "//*[@resource-id='com.android.chrome:id/url_bar'] | //*[@resource-id='com.android.chrome:id/search_box_text']"))
    # Clear url
    ue1.element(chrome_url).clear_text()
    ue1.element(chrome_url).click()
    # To download 1gb file
    ue1.element(chrome_url).click()
    ue1.element(chrome_url).fill_text(f"http://testfiles.hostnetworks.com.au/{download_file_size}MB.iso")
    ue1.press_enter()
    download_button = androidLocator(xpath("//*[@text='Download']"))
    if ue1.element(download_button).isElementPresent(3):
        ue1.element(download_button).click()
    done_button = androidLocator(xpath("//*[@text='Done'] | //*[@text='done']"))
    if ue1.element(done_button).isElementPresent(3):
        ue1.element(done_button).click()
    more_options_icon = androidLocator(xpath(
        "//*[@resource-id='com.android.chrome:id/menu_badge'] | //*[@resource-id='com.android.chrome:id/menu_button']"))
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
    DriverUtilities.kill_appium_server()


class MessagingProcess():

    def __init__(self, mobile_driver):
        self.messaging_page_obj = MessagingPage(mobile_driver)

    def launch_messages(self):
        self.messaging_page_obj.mobile.activate_app("com.samsung.android.messaging")

    def send_sms(self, message, phone_number):
        self.messaging_page_obj.click_on_compose_icon()
        self.messaging_page_obj.enterRecipientNumber(phone_number)
        self.messaging_page_obj.enterMessage(message)
        self.messaging_page_obj.clickOnSendButton()

    def verify_sms_is_displayed(self, message):
        if len(message) > 15:
            self.messaging_page_obj.select_latest_message_which_contains_text(message[:15])
        else:
            self.messaging_page_obj.select_latest_message_which_contains_text(message)
        self.messaging_page_obj.verify_if_message_is_present(message)

    def close_messages(self):
        self.messaging_page_obj.mobile.terminate_app("com.samsung.android.messaging")


class MessagingPage():

    def __init__(self, mobile_driver):
        self.mobile = mobile_driver
        self.compose_icon = androidLocator(xpath("//*[@contentDescription='Compose new message'] | //android.widget.ImageButton[@content-desc='Compose new message']"))
        self.message_textbox = androidLocator(xpath("//*[contains(@resource-id,'message_edit_text')]"))
        self.recipient_textbox = androidLocator(xpath("//*[contains(@resource-id,'recipients_editor_to')]"))
        self.send_button = androidLocator(xpath("//*[contains(@resource-id,'send_button')]"))
        self.back_arrow = androidLocator(xpath("//*[contains(@resource-id,'composer_up')]"))
        self.latest_message_with_content = lambda messageContent: \
            androidLocator(xpath(f"(//*[contains(@resource-id,'text_content')][contains(@text,'{messageContent}')])[1]"))
        self.message_content_in_conversation_screen = lambda messageContent: \
            androidLocator(xpath(f"//*[contains(@resource-id,'content_text_view')][contains(@text, '{messageContent}')]"))
        self.options_in_message_screen = androidLocator(xpath("//*[contains(@resource-id,'composer_setting_button')]"))
        self.delete_messages_option = androidLocator(xpath("//*[@text='Delete messages']"))
        self.select_all_radio_button_for_deleting_message = androidLocator(xpath("//*[contains(@resource-id,'bubble_all_select_checkbox')]"))
        self.delete_icon = androidLocator(xpath("//*[contains(@resource-id,'delete')]//*[@text='Delete']"))
        self.delete_button_from_popup = androidLocator(xpath("//*[contains(@resource-id,'button')][@text='Delete']"))

    def click_on_compose_icon(self):
        self.mobile.element(self.compose_icon).click()

    def enterMessage(self, message):
        self.mobile.element(self.message_textbox).fill_text(message)

    def enterRecipientNumber(self, recipient_ph_number):
        self.mobile.element(self.recipient_textbox).fill_text(recipient_ph_number)
        self.mobile.hide_keyboard_if_it_is_dispayed()

    def clickOnSendButton(self):
        self.mobile.element(self.send_button).click()

    def clickOnBackArrow(self):
        self.mobile.element(self.back_arrow).click()

    def select_latest_message_which_contains_text(self, message):
        self.mobile.element(self.latest_message_with_content(message)).click()

    def isMessagePresent(self, message):
        return self.mobile.element(self.message_content_in_conversation_screen(message)).is_element_present()

    def verify_if_message_is_present(self, message):
        self.mobile.element(self.message_content_in_conversation_screen(message)).validateElementIsPresent()

