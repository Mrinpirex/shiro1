import aiohttp
import asyncio
from bs4 import BeautifulSoup

# async def batch_ep(series_url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(series_url) as response:
#             html_content = await response.text()
#             soup = BeautifulSoup(html_content,'html.parser')
#             batch_element = soup.find('a', text=lambda t: 'All Episodes Batch' in t)

#             # Extract the href attribute
#             batch_url = batch_element['href'] if batch_element else None
            

#             print(batch_url)
            
            
# asyncio.run(batch_ep('https://episodes.modpro.co/archives/83510'))



