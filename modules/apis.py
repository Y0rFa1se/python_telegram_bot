from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    await update.message.reply_text(text)

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

async def edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE, new_text: str):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(new_text)

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str, file_name: str):
    await update.message.reply_document(document=open(file_path, "rb"), filename=file_name)

async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE, image_url: str):
    await update.message.reply_photo(photo=image_url)

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_url: str):
    await update.message.reply_video(video=video_url)

async def send_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, audio_url: str):
    await update.message.reply_audio(audio=audio_url)

async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    text = update.message.text
    if text:
        return text
    else:
        return None

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    file = update.message.document
    if file:
        file_path = await file.get_file().download()
        return file_path
    
    else:
        return None
    
async def send_inline_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, keys: dict[str, str]):
    keyboard = []

    for callback, keyword in keys.items():
        keyboard.append([InlineKeyboardButton(keyword, callback_data=callback)])

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def inline_keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, pattern: str, func, error_message: str = "Unknown pattern."):
    query = update.callback_query
    await query.answer()

    if query.data == pattern:
        await func(query, context)
        return True
        
    else:
        await edit_text(update, context, error_message)
        return False