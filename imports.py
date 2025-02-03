from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import TelegramError
import random
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
from psycopg2 import sql, errors
from loguru import logger
import matplotlib.pyplot as plt
from PIL import Image
from openai import OpenAI

from config import *
from db import Database

# from vocabulary import *

logger.add("file.log", rotation="1 MB", format="{time} {level} {message}", level="DEBUG")

# VARIABLES
user_data = {}
propriétaires = ['krsukhorukov']
admins = []
