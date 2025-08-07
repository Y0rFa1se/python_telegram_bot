from modules.__apis__ import *
from modules.__decorators__ import command, callback

from telegram import Update

@command("test")
async def test_command(update: Update):
    await update.message.reply_text("This is a test command.")