import os
import time
from datetime import datetime

import pandas as pd
from pandas import DataFrame
from google.cloud import storage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from secret_manager import access_secret_version
from helpers import get_vm_custom_envs

footy_username = get_vm_custom_envs("FOOTY_USERNAME")
footy_key = access_secret_version()

path = Path("/home/nicholasutikal/load_footy_import/auto_download_files")


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {"download.default_directory": r"{}".format(str(path))}
    # chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def clean_dir(path: str):
    mydir = path
    filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]
    for f in filelist:
        os.remove(os.path.join(mydir, f))


def read_storage(path: str):
    mydir = path
    filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]

    my_dataframe_list = []

    for file in filelist:
        my_dataframe_list.append(pd.read_csv(file))

    df = pd.concat(my_dataframe_list)
    df = df.dropna(how='all')
    df.columns = [x.replace(' ', '_').replace('-', '_').replace('(', '_').replace(')', '_') for x in df.columns]

    return df


def write_data(df: DataFrame):
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(get_vm_custom_envs("SINK"))

    csv_name = "data-import-{}.csv".format(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    bucket.blob(csv_name).upload_from_string(df.to_csv(header=0, index=0), "text/csv")
    print("Successfully imported, cleaned and exported match stats to {}".format(bucket))


def app():
    clean_dir(str(path))

    USERNAME = footy_username  # Your username
    PASSWORD = footy_key  # Your password

    driver = webdriver.Chrome(chrome_options=set_chrome_options())
    driver.get('https://footystats.org/login')

    time.sleep(5)

    search_box = driver.find_element_by_id("username")
    search_box.send_keys(USERNAME)

    search_box = driver.find_element_by_id("password")
    search_box.send_keys(PASSWORD)

    driver.find_element_by_id("register_submit").click()

    time.sleep(5)  # Let the user actually see something!

    # germany teams
    driver.get('https://footystats.org/c-dl.php?type=teams&comp=6192')  # Sample download 1
    time.sleep(3)
    # germany matches
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6192')  # Sample download 2
    # england matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6135')  # Sample download 2
    # spain matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6790')  # Sample download 2
    # italy matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6198')  # Sample download 2
    # france matches
    time.sleep(3)
    driver.get('https://footystats.org/c-dl.php?type=matches&comp=6019')  # Sample download 2

    time.sleep(5)

    driver.close()
    driver.quit()

    print('Success!')
    return None


if __name__ == "__main__":
    app()
    df = read_storage(str(path))
    write_data(df)
