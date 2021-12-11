from appium.webdriver.common.mobileby import MobileBy
from typing import Tuple

__MobileLocator = dict(android=Tuple[str, str], ios=Tuple[str, str])


def xpath(locator: str):
    return (MobileBy.XPATH, locator)


def id(locator: str):
    return (MobileBy.ID, locator)


def tagName(locator: str):
    return (MobileBy.TAG_NAME, locator)


def className(locator: str):
    return (MobileBy.CLASS_NAME, locator)


def cssSelector(locator: str):
    return (MobileBy.CSS_SELECTOR, locator)


def linkText(locator: str):
    return (MobileBy.LINK_TEXT, locator)


def name(locator: str):
    return (MobileBy.NAME, locator)


def partialLinkText(locator: str):
    return (MobileBy.PARTIAL_LINK_TEXT, locator)


def accessibilityId(locator: str):
    return (MobileBy.ACCESSIBILITY_ID, locator)


def androiDataMatcher(locator: str):
    return (MobileBy.ANDROID_DATA_MATCHER, locator)


def androidUIAutomator(locator: str):
    return (MobileBy.ANDROID_UIAUTOMATOR, locator)


def androidViewMatcher(locator: str):
    return (MobileBy.ANDROID_VIEW_MATCHER, locator)


def androidViewTag(locator: str):
    return (MobileBy.ANDROID_VIEWTAG, locator)


def iosClassChain(locator: str):
    return (MobileBy.IOS_CLASS_CHAIN, locator)


def iosPredicate(locator: str):
    return (MobileBy.IOS_PREDICATE, locator)


def iosUIAutomation(locator: str):
    return (MobileBy.IOS_UIAUTOMATION, locator)


def windowUIAutomation(locator: str):
    return (MobileBy.WINDOWS_UI_AUTOMATION, locator)


def image(imagePath: str):
    return (MobileBy.IMAGE, imagePath)


def mobileAppLocator(androidLocator: __MobileLocator or None = None, iosLocator: __MobileLocator or None = None):
    if androidLocator is None and iosLocator is None:
        raise Exception('Both android and ios locators are none, atleast one locator should be specified')
    return dict(android=androidLocator, ios=iosLocator)


def androidLocator(locator: __MobileLocator):
    return mobileAppLocator(androidLocator=locator)


def iosLocator(locator: __MobileLocator):
    return mobileAppLocator(iosLocator=locator)