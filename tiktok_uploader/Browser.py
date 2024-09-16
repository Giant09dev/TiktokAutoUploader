from .cookies import load_cookies_from_file, save_cookies_to_file
from fake_useragent import UserAgent, FakeUserAgentError
import undetected_chromedriver as uc
import threading, os
from selenium_stealth import stealth  # Importing selenium-stealth

WITH_PROXIES = False
CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_DRIVER_PATH = r"C:\Program Files\WebDriver\chromedriver-win64\chromedriver.exe"

class Browser:
    
    __instance = None

    @staticmethod
    def get():
        if Browser.__instance is None:
            with threading.Lock():
                if Browser.__instance is None:
                    Browser.__instance = Browser()
        return Browser.__instance

    def __init__(self):
        if Browser.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Browser.__instance = self
        self.user_agent = ""
        options = uc.ChromeOptions()
        options.binary_location = CHROME_BINARY_PATH

        # Proxies not supported on login.
        # if WITH_PROXIES:
        #     options.add_argument('--proxy-server={}'.format(PROXIES[0]))

        self._driver = uc.Chrome(options=options)
        from selenium_stealth import stealth

        # Apply stealth settings after initializing the driver
        stealth(self._driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            fix_hairline=True,
            use_stealth=True)
        self.with_random_user_agent()

    def with_random_user_agent(self, fallback=None):
        """Set random user agent."""
        try:
            self.user_agent = UserAgent().random
            print(f"Using User Agent: {self.user_agent}")  # Debugging line
        except FakeUserAgentError as e:
            if fallback:
                self.user_agent = fallback
            else:
                raise e

    @property
    def driver(self):
        return self._driver

    def load_cookies_from_file(self, filename):
        cookies = load_cookies_from_file(filename)
        for cookie in cookies:
            self._driver.add_cookie(cookie)
        self._driver.refresh()

    def save_cookies(self, filename: str, cookies:list=None):
        save_cookies_to_file(cookies, filename)


if __name__ == "__main__":
    import os
    print(os.path.dirname(os.path.abspath(__file__)))