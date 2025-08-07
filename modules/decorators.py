from telegram import Update
from telegram.ext import ContextTypes

import os

def command(cmd):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            result = None
            if str(update.effective_chat.id).strip() == os.getenv("CHAT_ID"):
                result = await func(update)

            return result
        
        wrapper.command = cmd
        wrapper.decorator = "command"
        return wrapper
    return decorator
    
def callback(callback_data):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query

            result = None
            if str(query.message.chat.id).strip() == os.getenv("CHAT_ID"):
                await query.answer()

                if query.data == callback_data:
                    result = await func(update)
                    return result
                
                else:
                    await query.edit_message_text("‼️잘못된 요청입니다‼️")

            return result

        wrapper.decorator = "callback"
        return wrapper
    return decorator