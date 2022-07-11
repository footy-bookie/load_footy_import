import os
import time
from pathlib import Path

import pandas as pd
from google.cloud import storage
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

footy_username = os.getenv("FOOTY_USERNAME")

path = Path("/home/nicholasutikal/load_footy_import/auto_download_files")


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_prefs = {"download.default_directory": r"{}".format(str(path))}
    # chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def read_storage(path: str) -> tuple:
    # read, clean and return teams files
    mydir = path
    filelist = [f for f in os.listdir(mydir) if f.endswith(".csv") and "teams" in f]

    my_dataframe_list = []

    for f in filelist:
        my_dataframe_list.append(pd.read_csv(os.path.join(mydir, f)))

    df = pd.concat(my_dataframe_list)
    df = df.dropna(how='all')
    df.columns = [x.replace(' ', '_').replace('-', '_').replace('(', '_').replace(')', '_') for x in df.columns]

    # read and return match files
    filelist_match = [f for f in os.listdir(mydir) if f.endswith(".csv") and "matches" in f]

    for f in filelist_match:
        df_match = pd.read_csv(os.path.join(mydir, f))

    return df, df_match


def write_data(df: DataFrame, df_match: DataFrame) -> None:
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(os.getenv("SINK"))

    csv_name = "data-import-teams.csv"
    bucket.blob(csv_name).upload_from_string(df.to_csv(header=0, index=0), "text/csv")

    csv_name_match = "data-import-matches.csv"
    bucket.blob(csv_name_match).upload_from_string(df_match.to_csv(header=0, index=0), "text/csv")
    print("Successfully imported, cleaned and exported match stats to {}".format(str(bucket)))

    return None


def main() -> None:
    USERNAME = footy_username  # Your username
    PASSWORD = os.getenv("FOOTY_KEY")  # Your password

    driver = webdriver.Chrome(chrome_options=set_chrome_options())
    driver.get('https://footystats.org/login')

    time.sleep(5)
    print(driver)
    search_box = driver.find_element_by_id("username")
    search_box.send_keys(USERNAME)

    search_box = driver.find_element_by_id("password")
    search_box.send_keys(PASSWORD)

    driver.find_element_by_id("register_submit").click()

    time.sleep(5)  # Let the user actually see something!

    # germany teams
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6192')
    time.sleep(3)
    driver.get_screenshot_as_file("screenshot.png")
    # germany matches
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6192')
    # england teams
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6135')
    # spain teams
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6211')
    # italy teams
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6198')
    # france teams
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6019')

    time.sleep(5)
    driver.close()
    driver.quit()
    print('Success!')

    return None


if __name__ == "__main__":
    main()
    df, df_match = read_storage(str(path))
    write_data(df, df_match)
