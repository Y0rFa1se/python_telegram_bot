from telegram.ext import Application
from dotenv import load_dotenv

from pathlib import Path
import pkgutil
import importlib
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def load_modules(app: Application):
    modules_path = Path("modules")

    for finder, name, ispkg in pkgutil.iter_modules([modules_path]):
        try:
            module = importlib.import_module(f"{modules_path}.{name}")
            module.setup(app)

        except Exception as e:
            print(f"Error loading module {name}: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    load_modules(app)

    app.run_polling()

if __name__ == '__main__':
    main()