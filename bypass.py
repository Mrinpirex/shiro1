from selenium.webdriver.common.by import By
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            # driver =webdriver.Firefox()

            add_extension_path = fr'{current_dir}/extension/ublock_origin-1.57.2.xpi'
                
            driver.install_addon(add_extension_path)
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
        
        start_verify_btn = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.block > a:nth-child(1) > h5:nth-child(1)'))
        )
        start_verify_btn.click()

        click_here_btn1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#verify_button2'))
        )
        click_here_btn1.click()

        click_here_btn2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#verify_button'))
        )
        click_here_btn2.click()
        
        time.sleep(10)
        
        down_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#two_steps_btn'))
        )
        down_url = down_btn.get_attribute('href')
        
        driver.get(down_url)
        
        WebDriverWait(driver, 10).until(
            EC.url_changes(down_url)
        )
        curr_url = driver.current_url
        
    except Exception as error:
        logging.error(f'{error} while bypassing {url}')

    finally:
        if driver is not None:
            driver.quit()
    return curr_url

def bypass_modrefer(modrefer_urls):
    driver = None
    curr_url = None
    try:
        driver = get_driver()
        driver.get(modrefer_urls)
        time.sleep(1.8)
        curr_url = driver.current_url
    
    except Exception as error:
        logging.error(f'{error} while bypassing modrefer')

    finally:
        if driver is not None:
            driver.quit()
    return curr_url
    
async def process_urls(urls: list[str], mode: str) -> list[str] | str:
    try:
        results = []
        processes = 3
        # Process URLs in batches of 2 to limit memory usage
        for i in range(0, len(urls), processes):
            sublist = urls[i:i + processes]
            logging.info(f"Processing sublist of URLs: {sublist}")
            if mode == 'tech':
                sublist_results = ThreadPool(len(sublist)).map(shorturl_bypass, sublist)
            elif mode == 'refer':
                sublist_results = ThreadPool(len(sublist)).map(bypass_modrefer, sublist)
                for j, sub_res in enumerate(sublist_results):
                    if 'archives' not in sub_res:
                        print(j, sublist[j])
                        sublist_results[j] = bypass_modrefer(sublist[j])#reprocess this URL (remove this block if not needed)
                                            
            results.extend(sublist_results)
        return results
    
    except ConnectionError as e:
        logging.error(f"Connection error: {e}. Retrying...")
        time.sleep(5)  # Delay before retrying
        return await process_urls(urls)
    
    except Exception as error:
        logging.error(f'{error} while processing bypass urls')
        return ["error processing url" for _ in range(len(urls))]
    
# if __name__ == '__main__':
#     shorturl_bypass('https://tech.unblockedgames.world/?sid=VWNwbWlPV1lMWFcwa1ZDb1dxQVBZaUNaVzN6a3ZDbmxWa3QyV1FzSENyN1YvS2phYXBUWWhPZURxUm1LSFBqcGNPME81N1ZaSFUybzBZMC9ydVcxTHp2d2dDRW5EbXVaVFdyVXFJSVFqM1B4eHJLNkM2TkQ4Q25BM3ZxSmlBOHlteENSRVVXRytlTmI4diszMXQ5dnl4T2xZUjhud3dqVkNUVTlLSmtMdHRzN2xGc2VwaFhYbTlJVUNUVG55R2FtKzlzc2tzcGs5YXZUZUtOSitIN3ZoeEd3UGFQMVQ0VTVkd1lPckdyL2xXS1J4Ym1haGVnMEo0eUFZOWMzaHJzTkIzUkd4NXp2d09QSHY0WkVLbG5GK1RXL21FNDNOTnNnclZCQlEydGZMcmw3dk9JY0xSamdOZ21zbnhTY1RTOWI=')