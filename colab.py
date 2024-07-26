from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from multiprocessing.pool import ThreadPool
from selenium import webdriver
import threading
import time
import os


import logging
logging.basicConfig(
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
current_dir = os.getcwd()
threadLocal = threading.local()

def get_driver():
    try:
        driver = getattr(threadLocal, 'driver', None)
        if driver is None:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Firefox(options=options)
            driver.install_addon('/content/ublock_origin-1.57.2.xpi', temporary=True)

            setattr(threadLocal, 'driver', driver)
        return driver
    except Exception as error:
        logging.error(f'{error} while creating driver instance')

def shorturl_bypass(url):
    driver = None
    curr_url = None
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(20)
        start_verify_btn = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.block > a:nth-child(1) > h5:nth-child(1)')))
        start_verify_btn.click()

        
        # Wait for click_here_btn1 to be visible
        click_here_btn1 = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#verify_button2')))
        click_here_btn1.click()

        # Wait for click_here_btn2 to be clickable
        click_here_btn2 = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#verify_button')))
        click_here_btn2.click()

        # Wait for down_btn to be clickable
        down_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#two_steps_btn')))
        down_url = down_btn.get_attribute('href')
        
        driver.get(down_url)
        time.sleep(6)
        curr_url = driver.current_url
        
    except Exception as error:
        driver.save_screenshot('error.png')
        logging.error(f'{error} while bypassing {url}')

    finally:
        if driver is not None:
            driver.quit()
    return curr_url



def process_urls(urls) -> list[str] | str:
    try:        
        results = ThreadPool(len(urls)).map(shorturl_bypass, urls)
        return results
    except Exception as error:
        logging.error(f'{error} while processing bypass urls')
        return ["error processing url" for _ in range(len(urls))]