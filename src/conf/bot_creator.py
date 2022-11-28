from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv
from pathlib import Path


storage = MemoryStorage()

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = Path(BASE_DIR, 'conf', '.env')
load_dotenv(dotenv_path)

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
