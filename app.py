from telegram.ext import Application
from dotenv import load_dotenv

import os

from loader import load_modules

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    load_modules(app)

    app.run_polling()

if __name__ == '__main__':
    main()