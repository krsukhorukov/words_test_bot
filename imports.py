import sqlite3
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import pandas as pd

from config import *
from vocabulary import *

# VARIABLES
user_data = {}
only_admins = False
propriétaires = ['krsukhorukov']
admins = []