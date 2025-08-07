from modules.apis import *
from modules.decorators import command, callback

from telegram import Update

@command("test")
async def test_command(update: Update):
    print("Test command executed")
    await update.message.reply_text("This is a test command.")