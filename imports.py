from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import TelegramError
import random
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql, errors
from loguru import logger

from config import *
from db import VocabularyDatabase
# from vocabulary import *

logger.add("file.log", rotation="1 MB", format="{time} {level} {message}", level="DEBUG")

# VARIABLES
user_data = {}
only_admins = True
propriétaires = ['krsukhorukov']
admins = []
