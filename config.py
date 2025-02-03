import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_KEY = os.getenv('TEMP_OPENAI_API_KEY')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD =os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
CHAT_ID = os.getenv('CHAT_ID')
