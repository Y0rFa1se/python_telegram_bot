from telegram import Update
from telegram.ext import ContextTypes

def command(cmd):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            result = await func(update)
            return result
        
        wrapper.command = cmd
        return wrapper
    return decorator
    
def callback(callback_data):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            await query.answer()

            if query.data == callback_data:
                result = await func(update)
                return result
            
            else:
                await query.edit_message_text("‼️잘못된 요청입니다‼️")

        return wrapper
    return decorator