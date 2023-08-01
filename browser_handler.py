from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import undetected_chromedriver as uc
from selenium import webdriver
from random_sleep import RandomSleep


class BrowserHandler:

    def __init__(self):
        self._driver = None
        self._tab_index_max = 0
        self._tab_index_current = 0
        self.debug = False

    @property
    def driver(self):
        return self._driver

    @property
    def tab_index_max(self):
        return self._tab_index_max

    @property
    def tab_index_current(self):
        return self._tab_index_current

    def browser_import_cookies(self, cookie_data: dict, url: str) -> bool:
        try:
            self.driver.get(url)
            for cookie in cookie_data:
                self.driver.add_cookie(cookie)
            return True
        except Exception as e:
            if self.debug:
                print(e)
            return False

    def browser_start(self, headless: bool = False) -> bool:
        if self._driver is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--mute-audio")
            self._driver = uc.Chrome(headless=headless, use_subprocess=False, options=chrome_options,
                                     driver_executable_path="chromedriver/chromedriver.exe")
            return True
        return False

    def browser_close(self) -> bool:
        if self._driver is not None:
            self._driver.quit()
            self._driver = None
            return True
        return False

    def browser_open_new_tab(self) -> None:
        self._driver.switch_to.new_window('tab')
        self._tab_index_max += 1
        self._tab_index_current = self._tab_index_max

    def browser_close_tab(self, tab_num: int) -> bool:
        if self.browser_switch_to_tab(tab_num):
            self._driver.close()
            self._tab_index_max -= 1
            return True
        return False

    def browser_switch_to_tab(self, tab_num: int) -> bool:
        if (0 <= tab_num <= self._tab_index_max) and (tab_num != self._tab_index_current):
            self._driver.switch_to.window(self._driver.window_handles[tab_num])
            self._tab_index_current = tab_num
            return True
        return False

    def browser_goto_page(self, url: str) -> None:
        self._driver.get(url)

    def element_is_present(self, xpath: str, timeout: float = 5) -> ec.WebElement:
        wait = WebDriverWait(self._driver, timeout)
        try:
            return wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            if self.debug:
                print(e)

    def element_is_invisible_present(self, xpath: str, timeout: float = 5) -> ec.WebElement:
        wait = WebDriverWait(self._driver, timeout)
        try:
            return self._driver.execute_script('return document.querySelector("' + xpath + '")')
        except Exception as e:
            if self.debug:
                print(e)

    def element_is_enabled(self, xpath: str, timeout: float = 5) -> ec.WebElement:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return element.is_enabled()
        except Exception as e:
            if self.debug:
                print(e)

    def element_click(self, xpath: str, timeout: float = 5) -> bool:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            element.click()
            RandomSleep.sleep(4, 3)
            return True
        except Exception as e:
            if self.debug:
                print(e)

    def element_get_name(self, xpath: str, attribute: str = 'class', timeout: float = 5) -> str:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return element.get_attribute(attribute)
        except Exception as e:
            if self.debug:
                print(e)

    def element_get_text(self, xpath: str, timeout: float = 5) -> str:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return self._driver.execute_script('return arguments[0].textContent;', element)
        except Exception as e:
            if self.debug:
                print(e)

    def elements_is_any_present(self, xpath: str):
        script = "return document.evaluate('" + xpath.replace("'", "\\'") + "', document, null, XPathResult.ANY_TYPE," \
                                                                            " null).iterateNext() !== null;"
        return self._driver.execute_script(script)

    def elements_click_all(self, xpath: str):
        script = "var buttons = document.evaluate('" + xpath.replace("'", "\\'") + "', document, null, " + \
                 "XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);for (var i = 0; i < buttons.snapshotLength; i++)" + \
                 " { buttons.snapshotItem(i).click(); }"
        self._driver.execute_script(script)
