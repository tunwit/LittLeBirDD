import json
from dotenv import load_dotenv
import logging
import os

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
