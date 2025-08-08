from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup

class APP_SESSION:
    def __init__(self):
        self.data = dict()

def markup_keyboard(keys: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = []

    for row in keys:
        keyboard_tmp = []
        for button_text, callback_data in row:
            keyboard_tmp.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.append(keyboard_tmp)

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def is_last_message(update: Update) -> bool:
    return update.message is not None

async def is_last_callback(update: Update) -> bool:
    return update.callback_query is not None

async def send_message(update: Update, text: str) -> Message:
    if await is_last_callback(update):
        return await update.callback_query.message.reply_text(text)
    elif await is_last_message(update):
        return await update.message.reply_text(text)

async def delete_query_message(update: Update):
    await update.message.delete()

async def delete_message(message: Message):
    await message.delete()

async def edit_message(message: Message, text: str):
    await message.edit_text(text)

async def send_file(update: Update, file_path: str, file_name: str):
    try:
        with open(file_path, "rb") as file:
            await update.message.reply_document(file, filename=file_name)
    except FileNotFoundError:
        await send_message(update, "File not found.")
    except Exception as e:
        await send_message(update, f"Error: {e}")

async def send_image(update: Update, image_url: str):
    if await is_last_callback(update):
        await update.callback_query.message.reply_photo(photo=image_url)
    elif await is_last_message(update):
        await update.message.reply_photo(photo=image_url)

async def send_video(update: Update, video_url: str):
    if await is_last_callback(update):
        await update.callback_query.message.reply_video(video=video_url)
    elif await is_last_message(update):
        await update.message.reply_video(video=video_url)

async def send_audio(update: Update, audio_url: str):
    if await is_last_callback(update):
        await update.callback_query.message.reply_audio(audio=audio_url)
    elif await is_last_message(update):
        await update.message.reply_audio(audio=audio_url)

async def get_last_message(update: Update) -> str | None:
    try:
        query = update.message.text.split()
        text = ""
        for word in query[1:]:
            text += word + " "

        return text[:-1] if text else None

    except AttributeError:
        return None

async def get_last_callback(update: Update) -> str | None:
    try:
        return update.callback_query.data
    except AttributeError:
        return None

async def get_last_file(update: Update) -> str | None:
    try:
        return await update.message.document.get_file().download()
    except AttributeError:
        return None
    
async def send_inline_keyboard(update: Update, text: str, keys: dict[str, str]):
    """
    keys = [
        [("button_text", "callback_data")],
        [("button_text_2", "callback_data_2"), ("button_text_3", "callback_data_3")]
    ]
    """
    reply_markup = markup_keyboard(keys)

    if await is_last_callback(update):
        await update.callback_query.message.reply_text(text, reply_markup=reply_markup)
    elif await is_last_message(update):
        await update.message.reply_text(text, reply_markup=reply_markup)

async def edit_inline_keyboard(update: Update, text: str, keys: dict[str, str]):
    """
    keys = [
        [("button_text", "callback_data")],
        [("button_text_2", "callback_data_2"), ("button_text_3", "callback_data_3")]
    ]
    """
    reply_markup = markup_keyboard(keys)
    await update.callback_query.message.edit_text(text, reply_markup=reply_markup)