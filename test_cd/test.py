from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

try:
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://footystats.org/login")
    driver.get_screenshot_as_file("screenshot.png")
    time.sleep(3)

    s = driver.find_element_by_id("username")
    assert s.is_displayed() is True
    print("ok")
    driver.quit()
except Exception as ex:
    print(ex)
