from modules.apis import *
from modules.decorators import command, callback

from telegram import Update

@command("test")
async def test_command(update: Update):
    print("Test command executed")
    await send_message(update, "Test")

@command("test_save")
async def test_save(update: Update):
    msg = await get_last_message(update)
    print(msg)
    APP_SESSION.test_data = msg

@command("test_get")
async def test_get(update: Update):
    msg = APP_SESSION.test_data
    print(msg)
    await send_message(update, f"Saved data: {msg}")

@command("test_keyboard")
async def test_keyboard(update: Update):
    keys = [
        [("test_button", "test_callback")]
    ]
    await send_inline_keyboard(update, "Test", keys)

@command("test_delete_query")
async def test_delete_query(update: Update):
    print("Test delete executed")
    await delete_query_message(update)

@command("test_delete")
async def test_delete(update: Update):
    msg = await send_message(update, "This message will be deleted")
    print("Test delete executed")
    await delete_message(msg)

@command("test_edit")
async def test_edit(update: Update):
    msg = await send_message(update, "This message will be edited")
    print("Test edit executed")
    await edit_message(msg, "Edited text")
    await delete_query_message(update)

@callback("test_callback")
async def test_callback(update: Update):
    print("Test callback executed")
    keys = [
        [("test_button_2", "test_callback_2")]
    ]
    await send_inline_keyboard(update, "Test", keys)

@callback("test_callback_2")
async def test_callback_2(update: Update):
    print("Test callback2 executed")
    keys = [
        [("test_button_3", "test_callback_3")]
    ]
    await edit_inline_keyboard(update, "Test", keys)

@callback("test_callback_3")
async def test_callback_3(update: Update):
    print("Test callback3 executed")
    keys = [
        [("test_button_2", "test_callback_2")]
    ]
    await edit_inline_keyboard(update, "Test", keys)