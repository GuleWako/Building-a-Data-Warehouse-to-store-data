import nest_asyncio
import os
import csv
import re
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
from scripts.logging import logger
# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load environment variables from .env file
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')

# Initialize the Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# Define the CSV file to store the data
csv_file = 'telegram_data.csv'
def write_to_csv(message_date, message_id, message_text):
    """Append a message to the CSV file."""
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            message_date, 
            message_id,
            message_text.strip(),
           
         
        ])

# Function to scrape messages from Telegram channels
async def scrape_telegram_channels(channel):
    """
    Scrapes historical messages from a Telegram channel and saves the data to a CSV file.
    Args:
    channel : A Telegram channel username to scrape.
    """
    media_dir='photos'
    await client.start() 
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['message_date', 'message_id', 'message_description'])  # Write CSV header

    for channel_username in channel:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        # logger.info(f"Scraping historical data from {channel_username} ({channel_title})...")
        print(f"Scraping historical data from {channel_username} ({channel_title})...")

        async for message in client.iter_messages(entity, limit=30):
            if message.message:
                text_reg = r'[\u1200-\u137F0-9a-zA-Z\+\-_\.\:/\?\&=%]+'
                url_reg = r'http[s]?://\S+|www\.\S+'
                
                # text_reg = r'[\u1200-\u137F0-9a-zA-Z\+\-_]+'
                mess_text = ' '.join(re.findall(text_reg, message.message))
                mess_text = re.sub(url_reg, '', mess_text)
                
                
                # media_file = '[No Media]'
                if channel_username in ['@CheMed123','@lobelia4cosmetics']: 
                    if message.media and hasattr(message.media, 'photo'):
                            # Create a unique filename for the photo
                            filename = f"{channel_username}_{message.id}.jpg"
                            media_path = os.path.join(media_dir, filename)
                            # Download the media to the specified directory if it's a photo
                            await client.download_media(message.media, media_path)
                            media_file = media_path
                if mess_text.strip(): 
                    message_date = message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else '[No Date]'
                    sender_id = message.sender_id if message.sender_id else '[No Sender ID]'
                    write_to_csv(message_date, message.id, mess_text)
            
        logger.info(f"Finished scraping {channel_username}")
        # print(f"Finished scraping {channel_username}")
    logger.info("Listening for real-time messages...")
    # print("Listening for real-time messages...")
    client.run_until_disconnected() 
    

channels = ['@DoctorsET','@lobelia4cosmetics','@yetenaweg','@EAHCI','@CheMed123']
# Real-time message handler to update the CSV file when new messages arrive
@client.on(events.NewMessage(chats=channels)) 
async def real_time_message_handler(event):
    message = event.message.message
    if message:
        text_reg = r'[\u1200-\u137F0-9a-zA-Z\+\-_\.\:/\?\&=%]+'
        url_reg = r'http[s]?://\S+|www\.\S+'
        
        # text_reg = r'[\u1200-\u137F0-9a-zA-Z\+\-_]+'
        mess_text = ' '.join(re.findall(text_reg, message.message))
        mess_text = re.sub(url_reg, '', mess_text)
        
        if mess_text.strip():
            message_date = event.message.date.strftime('%Y-%m-%d %H:%M:%S')
            sender_id = event.message.sender_id if event.message.sender_id else '[No Sender ID]'
            write_to_csv(message_date, sender_id, event.message.id, mess_text)
            logger.info(f"New message added to CSV: {mess_text}")
            # print(f"New message added to CSV: {mess_text}")

def start_scraping(channel):
    """
    Wrapper function to start historical scraping and enable real-time message listening.
    Args:
    channel : A list of Telegram channel usernames to scrape.
    """
    
    logger.info("Scrapping data...")
    # print("Scrapping data...")
    # scrape_telegram_channels(channel) 
    asyncio.run(scrape_telegram_channels(channel))
    
      



