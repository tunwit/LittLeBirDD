import json
from dotenv import load_dotenv
import logging
import os
import requests
import sys

path = os.getcwd()

logger = logging.getLogger('littlebirdd')
with open("_config.json", "r") as f:
    config = json.load(f)

MODEL = config["model"]  # test for LittlePonYY | main for LittLeBirDD

if MODEL == 'main':
    load_dotenv('.env.production')
    logger.info('Load new .env.production')
elif MODEL == 'test':
    load_dotenv('.env.development')
    logger.info('Load new .env.development')
else:
    raise 'Unvalid bot MODEL'


LOCAL_LAVALINK = config[MODEL]['local_lavalink']
if LOCAL_LAVALINK:
    if not os.path.exists(f"lavalink"):
        os.makedirs(f"lavalink")
    logger.info("using Local Lavalink")
    if not os.path.isfile(f"lavalink\\Lavalink.jar"):
        try:
            logger.info('Downloading Lavalink.jar.')
            response = requests.get('https://github.com/lavalink-devs/Lavalink/releases/download/4.0.5/Lavalink.jar', stream=True)
            response.raise_for_status()
            with open(f"lavalink\\Lavalink.jar", 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logger.info('Lavalink success fully dowloaded')        
        except requests.exceptions.RequestException as e:
            logger.info(f'Fail to dowload Lavalike due to \n{e}')  
            sys.exit()

    if not os.path.isfile(f"lavalink\\application.yml"):
        try:
            logger.info('Downloading application.yml.')
            response = requests.get('https://raw.githubusercontent.com/tunwit/Lavalink/main/application.yml', stream=True)
            response.raise_for_status()
            with open(f"lavalink\\application.yml", 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logger.info('application.yml success fully dowloaded')        
        except requests.exceptions.RequestException as e:
            logger.info(f'Fail to dowload application.yml due to \n{e}')  
            sys.exit()


    if not os.path.isfile(f"start_lavalink.bat"):      
        with open(f'start_lavalink.bat', "w") as bat_file:
            bat_file.write(f"""start cmd.exe /k "cd lavalink && java -jar lavalink.jar""")   

CONFIG = config[MODEL] 
TOKEN = os.getenv('TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
LYRICSGENIUS = os.getenv('LYRICSGENIUS')
LAST_API_KEY = os.getenv('LAST_API_KEY')
LAST_API_SECRET = os.getenv('LAST_API_SECRET')
LAST_USERNAME = os.getenv('LAST_USERNAME')
LAST_PASSWORD = os.getenv('LAST_PASSWORD')
MONGO = os.getenv('MONGO')
