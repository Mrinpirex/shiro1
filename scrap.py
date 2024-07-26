#https://gist.github.com/miraculixx/2f9549b79b451b522dde292c4a44177b 

from bypass import process_urls
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
import logging
logging.basicConfig(
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def get_bypass_url(res_urls):
    logging.info(f'Bypassing urls: {res_urls}')
    if isinstance(res_urls, list):
        for url in res_urls:
            if 'https://tech.unblockedgames.world' in url and url is not None:
                driveurls_list = await process_urls(res_urls, 'tech')
                return driveurls_list
            elif 'https://driveseed.org' in url and url is not None:
                return res_urls
            else:
                logging.error('Unexpected error while processing list URLs')
        return []  # Return an empty list if no valid URL is found
    else:
        url = [res_urls]  # If res_urls is a single URL
        if 'https://tech.unblockedgames.world' in res_urls and res_urls is not None:
            driveurls_list = await process_urls(url, 'tech')
            return driveurls_list
        elif 'https://driveseed.org' in url and url is not None:
            return [res_urls]
        else:
            logging.error('get_bypass_url() : Unexpected error while processing single URLs')
        return []  # Return an empty list if no valid URL is found

                        

async def get_drivesurls(session: ClientSession,arc_url: list[str]) -> list[str] | None:#MOVIES AND SERIES ZIP 
    try:
        async with session.get(arc_url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, 'html.parser')
            if 'episodes' in arc_url:#ZIP & LIST SERIES
                button = soup.find('button', id=['allEpisodesButton', 'All Episodes Batch'])
                element = button.find_parent('a') if button else None                
            else:
                element = soup.find('a', class_='maxbutton-1 maxbutton maxbutton-fast-server-gdrive', href=True)#MOVIES

            if element:
                return element['href']
            else:
                return ['error while scraping driveseed single urls' for _ in range(len(arc_url))]
    except Exception as error:
        logging.error(f'get_drivesurls() : {error}')
        
async def bypass_modrefer_urls(modrefer_urls):
        res = await process_urls(modrefer_urls, 'refer')
        return res
        
async def get_modrefer_urls(page_content: BeautifulSoup) -> list[str]:
    non_uhd_elements = page_content.find_all('a', class_=['maxbutton-1 maxbutton maxbutton-download-links', 'maxbutton-23 maxbutton maxbutton-episode-links','maxbutton-24 maxbutton maxbutton-batch-zip'], href=True)
        
    urls = [url["href"] for url in non_uhd_elements]
    logging.info(f'Scraped archive urls: {urls}')

    return urls

async def get_series_archive_urls(session: ClientSession,arc_url: list[str]) -> list[str] | None:
        async with session.get(arc_url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content,'html.parser')
            batch_element = soup.find('a', text=lambda t: 'All Episodes Batch' in t)
            batch_url = batch_element['href'] if batch_element else None
            logging.info(f'Batch urls: {batch_url}')
            return batch_url


async def get_quality(page_content: BeautifulSoup) -> list[str]:
    try:
        qualities = ['480p', '720p', '1080p']
        desired_styles = ["text-align: center;","text-align: center; color: #008080;"]
        parse_quality = page_content.find_all(['span','h3','h4'],style=lambda value: value in desired_styles)
        # parse_quality = page_content.find(['h3','h4'], {"style": "text-align: center;"})
        unfiltered_text_list = [q.text for q in parse_quality if ('MB' in q.text) or ('GB' in q.text)]
        filtered_text_list = [text[text.find(quality):] for text in unfiltered_text_list for quality in qualities if quality in text]
        logging.info('Scraped Qualites')
        return filtered_text_list
    
    except Exception as error:
        logging.error(f'get_quality() : {error}')

async def get_ds_title(session: ClientSession, ds_urls: list[str]) -> list[str]:
    titles = []
    try:
        for ds_url in ds_urls:
            async with session.get(ds_url) as response:
                page_html = await response.text()
                page_content = BeautifulSoup(page_html, 'html.parser')
                title = page_content.find("title")
                if title:
                    titles.append(title.text)
                else:
                    titles.append('No title found')
        logging.info('Scraped Titles')
    except Exception as error:
        logging.error(f'get_ds_title() : {error}')
    return titles

async def get_title(page_content: BeautifulSoup) -> str:
    try:
        title = page_content.find("title")
        title_name = title.text.strip("Donwload")
        logging.info('Scraped Title')
        return title_name
    except Exception as error:
        logging.error(f'get_title() : {error} while scraping Title')

async def data_fetch(scrap_url: str) -> None:
    try:
        logging.info(f'Requesting {scrap_url}')
        async with ClientSession() as session:
            async with session.get(scrap_url) as response:
                html_content = await response.text()                    
                parse_html = BeautifulSoup(html_content,"html.parser")
                title = await get_title(parse_html) #GET TITLE
                qualities = await get_quality(parse_html) #GET QUALITY
                modrefer_urls = await get_modrefer_urls(parse_html) # GET ARCHIVE URLS
                archive_urls = await bypass_modrefer_urls(modrefer_urls)
                
                if "season" in scrap_url: 
                    tasks = [get_series_archive_urls(session,arc_url) for arc_url in archive_urls]
                else:
                    tasks = [get_drivesurls(session,arc_url) for arc_url in archive_urls]
                
                results = await asyncio.gather(*tasks)
                
                result_urls = [result_url for result_url in results if result_url is not None]
                
                bypass_url = await get_bypass_url(result_urls)
                
                return await data_format(title, qualities, bypass_url)
            
    except Exception as error:
        logging.error(f"data_fetch() : {error}")

async def data_format(title: str, qualites: list[str], down_urls: list[str]) -> str:
    try:
        logging.info('Formatting scrap data')
        data_dict = {
            'title':title
        } 
        formatted_url_msg = ''
        for quality,url in zip(qualites,down_urls):
            data_dict[quality] = url
        
        for key,value in data_dict.items():
            if key != 'title':
                formatted_url_msg += f'<i>{key}</i>:{value}\n\n'
                
        title = str(title).strip(" – MoviesMod – 480p Movies, 720p Movies, 1080p Movies").replace("||", "|")
        
        # logging.info(f'<b>{title}</b>\n' + formatted_url_msg)
        return f'<b>{title}</b>\n' + formatted_url_msg
    
    except Exception as error:
        logging.error(f'data_format() : {error}')
    
    
async def bypass_archive_urls(scrap_url: list[str]) -> str:
    try:
        async with ClientSession() as session:
            logging.info(f'Requesting {scrap_url}')
            
            formatted_msg = ''
            
            tasks = [get_drivesurls(session,arc_url) for arc_url in scrap_url]
                
            results = await asyncio.gather(*tasks)
            
            result_urls = [result_url for result_url in results if result_url is not None]
                    
            driveseed_urls = await get_bypass_url(result_urls)
            
            driveseed_title = await get_ds_title(session, driveseed_urls)
            
            if driveseed_title and driveseed_urls:
                for title, ds_url in zip(driveseed_title, driveseed_urls):
                        formatted_msg += f'<b>Filename</b>:<b>{title}</b>\n┗{ds_url}\n'
                return formatted_msg
            else:
                return "No URLs or titles found."
                        
    except Exception as error:
        logging.error(f'bypass_archive_urls() : {error}')
        return "An error occurred during processing."   

if __name__ == "__main__":
    asyncio.run(bypass_archive_urls(['https://links.modpro.blog/archives/101981', 'https://episodes.modpro.blog/archives/89144', 'https://episodes.modpro.blog/archives/82328']))    