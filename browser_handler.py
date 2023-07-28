from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import undetected_chromedriver as uc
from selenium import webdriver


class BrowserHandler:

    def __init__(self):
        self._driver = None
        self._tab_index = 0

    @property
    def driver(self):
        return self._driver

    @property
    def tab_index(self):
        return self._tab_index

    def browser_import_cookies(self, cookie_data: list, url: str) -> None:
        self.driver.get(url)
        for cookie in cookie_data:
            self.driver.add_cookie(cookie)

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
        self._driver.execute_script("window.open('', '_blank');")
        self._tab_index += 1

    def browser_close_tab(self, tab_num: int) -> bool:
        if self.browser_switch_to_tab(tab_num):
            self._driver.close()
            self._tab_index -= 1
            return True
        return False

    def browser_switch_to_tab(self, tab_num: int) -> bool:
        if 0 <= tab_num <= self._tab_index:
            self._driver.switch_to.window(self._driver.window_handles[tab_num])
            return True
        return False

    def browser_goto_page(self, url: str) -> None:
        self._driver.get(url)

    def element_is_present(self, xpath: str, timeout: float = 5) -> ec.WebElement:
        wait = WebDriverWait(self._driver, timeout)
        try:
            return wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
        except Exception:
            pass

    def element_click(self, xpath: str, timeout: float = 5) -> bool:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            element.click()
            return True
        except Exception:
            return False

    def element_get_name(self, xpath: str, timeout: float = 5) -> str:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return element.get_attribute('class')
        except Exception:
            pass

    def element_get_text(self, xpath: str, timeout: float = 5) -> str:
        wait = WebDriverWait(self._driver, timeout)
        try:
            element = wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return self._driver.execute_script('return arguments[0].textContent;', element)
        except Exception:
            pass
