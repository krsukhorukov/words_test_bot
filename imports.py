import sqlite3
from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import TelegramError
import random
import pandas as pd

from config import *
from vocabulary import *

# VARIABLES
group_id = chat_id
user_data = {}
only_admins = True
propriétaires = ['krsukhorukov']
admins = []