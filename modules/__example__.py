from modules.apis import *
from modules.decorators import command, callback

from telegram import Update

@command("help_test")
async def help_test(update: Update):
    await update.message.reply_text("This is a test command for help.")

@callback("help_test")
async def help_test_callback(update: Update):
    await update.message.reply_text("This is a test callback for help.")