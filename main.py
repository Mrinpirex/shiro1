from scrap import data_fetch, bypass_archive_urls
from pyrogram import Client, filters, types
from keep_alive import keep_alive
from config import *
import asyncio
import logging

logging.basicConfig(
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    level=logging.INFO
)

# Create a logger
logger = logging.getLogger(__name__)

scrapbot = Client(
    'shirobot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def is_admin(user_id):
    return user_id in LIST_OF_ADMINS

async def process_archives_url(bot, msg, scrap_url):
    process_msg = await bot.send_message(chat_id=msg.chat.id, text='<i>scraping...</i>', reply_to_message_id=msg.id)
    try:
        scraped_result = await bypass_archive_urls(scrap_url)
        if scraped_result:
            logging.info("Link scraped...Sending result")
            await bot.edit_message_text(chat_id=process_msg.chat.id, message_id=process_msg.id, text=scraped_result)
            try:
                await bot.copy_message(
                    chat_id=DST_ID,
                    from_chat_id=msg.chat.id,
                    message_id=process_msg.id
                )
            except Exception as e:
                logging.error(f"Error occurred while forwarding the message: {e}")
    except Exception as e:
        logging.error(f"Error occurred while scraping: {e}")
        await bot.edit_message_text(chat_id=process_msg.chat.id, message_id=process_msg.id, text=f"Error: {e}")

async def process_scraping(bot, msg, scrap_url):
    process_msg = await bot.send_message(chat_id=msg.chat.id, text='<i>scraping...</i>', reply_to_message_id=msg.id)
    try:
        scraped_result = await data_fetch(scrap_url)
        if scraped_result:
            logging.info("Link scraped...Sending result")
            await bot.edit_message_text(chat_id=process_msg.chat.id, message_id=process_msg.id, text=scraped_result)
            try:
                await bot.copy_message(
                    chat_id=DST_ID,
                    from_chat_id=msg.chat.id,
                    message_id=process_msg.id
                )
            except Exception as e:
                logging.error(f"Error occurred while forwarding the message: {e}")
    except Exception as e:
        logging.error(f"Error occurred while scraping: {e}")
        await bot.edit_message_text(chat_id=process_msg.chat.id, message_id=process_msg.id, text=f"Error: {e}")

@scrapbot.on_message(filters.command('start') & filters.private)
async def start(bot, msg):
    await bot.send_message(chat_id=msg.chat.id, text=f"<i>Hi @{msg.from_user.username}\n/help to know more about me</i>", reply_to_message_id=msg.id)

@scrapbot.on_message(filters.command('help') & filters.private)
async def help(bot, msg):
    await bot.send_message(chat_id=msg.chat.id, text=f"<i>This bot can scrape links and bypass shorturls.\nSend me links with /scrape or /s to scrape links.</i>", reply_to_message_id=msg.id)

@scrapbot.on_message(filters.command(['scrape', 's']) & filters.private)
async def scrape(bot, msg):
    if await is_admin(msg.from_user.id):
        if msg.text not in ['/scrape', '/s']:
            scrap_url = str(msg.text).replace("/scrape", "").replace("/s", "").strip()
            if 'https://moviesmod' in scrap_url:
                await process_scraping(bot, msg, scrap_url)
        else:
            await bot.send_message(chat_id=msg.chat.id, text='<i>send with link</i> /scrape {url}', reply_to_message_id=msg.id)
    else:
        await bot.send_message(chat_id=msg.chat.id, text='<b>You are not AUTHORIZED!</b>', reply_to_message_id=msg.id)
        
@scrapbot.on_message(filters.command(['drive', 'd']) & filters.private)
async def archive(bot, msg):
    if await is_admin(msg.from_user.id):
        if msg.text not in ['/drive', '/d']:
            archives_urls = str(msg.text).replace('/drive', '').replace('/d', '').strip().split()
            a_urls =  [url for url in archives_urls if 'archives']
            await process_archives_url(bot, msg, a_urls)
            
        else:
            await bot.send_message(chat_id=msg.chat.id, text='<i>send with link</i> /archive {url}', reply_to_message_id=msg.id)
    else:
        await bot.send_message(chat_id=msg.chat.id, text='<b>You are not AUTHORIZED!</b>', reply_to_message_id=msg.id)


if __name__ == "__main__":
    keep_alive()
    asyncio.run(scrapbot.run())
    

