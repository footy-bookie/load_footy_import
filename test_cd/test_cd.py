import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

USERNAME = 'nichohelmut'  # Your username
PASSWORD = '80086'  # Your password


# CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver' # Insert the path of chromedriver (to be downloaded from "https://sites.google.com/a/chromium.org/chromedriver/downloads")

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return options


try:
    driver = webdriver.Chrome(chrome_options=set_chrome_options())

    driver.get('https://footystats.org/login');

    time.sleep(5)  # Let the user actually see something!

    search_box = driver.find_element_by_id('username')
    search_box.send_keys(USERNAME)
    search_box = driver.find_element_by_id('password')

    search_box.send_keys(PASSWORD)

    driver.find_element_by_id('register_submit').submit()

    time.sleep(5)  # Let the user actually see something!

    # germany teams
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6192');  # Sample download 1
    time.sleep(3)
    # germany matches
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6192');  # Sample download 2
    # england matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6135');  # Sample download 2
    # spain matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6790');  # Sample download 2
    # italy matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6198');  # Sample download 2
    # france matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6019');  # Sample download 2

    assert search_box.is_displayed() is True
    print("ok")
    driver.quit()
except Exception as ex:
    print(ex)
