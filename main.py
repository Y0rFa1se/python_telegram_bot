from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from dotenv import load_dotenv
import os
import sqlite3

# 환경 변수 로드
load_dotenv()

# 봇 토큰 (BotFather에서 받은 토큰을 여기 입력하세요)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 토큰이 비어있으면 에러 방지
if not BOT_TOKEN:
    print("❌ 에러: BOT_TOKEN을 설정해주세요!")
    print("1. @BotFather에게 /newbot 명령어 보내기")
    print("2. 봇 이름 설정하기") 
    print("3. 받은 토큰을 BOT_TOKEN 변수에 입력하기")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 인라인 키보드 만들기 (BotFather 스타일)
    keyboard = [
        [InlineKeyboardButton("API Token", callback_data="api_token"),
         InlineKeyboardButton("Edit Bot", callback_data="edit_bot")],
        [InlineKeyboardButton("Bot Settings", callback_data="bot_settings"),
         InlineKeyboardButton("Payments", callback_data="payments")],
        [InlineKeyboardButton("Transfer Ownership", callback_data="transfer"),
         InlineKeyboardButton("Delete Bot", callback_data="delete_bot")],
        [InlineKeyboardButton("« Back to Bot List", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Here it is: forrest @yf_test_bot.\nWhat do you want to do with the bot?",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("도움말: /start - 시작, /help - 도움말, /file - 파일 보내기")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"받은 메시지: {text}")

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

# 파일 보내기 함수들
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 텍스트 파일 보내기
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write("안녕하세요! 이것은 테스트 파일입니다.")
    
    await update.message.reply_document(document=open('test.txt', 'rb'), filename='테스트파일.txt')

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 사진 보내기 (URL 또는 파일)
    await update.message.reply_photo(photo='https://via.placeholder.com/300x200')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 받은 파일 정보 보기
    file = update.message.document
    await update.message.reply_text(f"파일 받음: {file.file_name} (크기: {file.file_size} bytes)")

# 버튼 클릭 처리
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # 버튼 클릭 응답
    
    if query.data == "api_token":
        await query.edit_message_text("🔑 API Token: 123456789:ABCdefGHijklMNopQRstuvWXyz")
    elif query.data == "edit_bot":
        await query.edit_message_text("✏️ Bot 편집 메뉴입니다.")
    elif query.data == "bot_settings":
        await query.edit_message_text("⚙️ Bot 설정 메뉴입니다.")
    elif query.data == "payments":
        await query.edit_message_text("💰 결제 설정 메뉴입니다.")
    elif query.data == "transfer":
        await query.edit_message_text("👥 소유권 이전 메뉴입니다.")
    elif query.data == "delete_bot":
        await query.edit_message_text("🗑️ 정말 봇을 삭제하시겠습니까?")
    elif query.data == "back":
        # 원래 메뉴로 돌아가기
        keyboard = [
            [InlineKeyboardButton("API Token", callback_data="api_token"),
             InlineKeyboardButton("Edit Bot", callback_data="edit_bot")],
            [InlineKeyboardButton("Bot Settings", callback_data="bot_settings"),
             InlineKeyboardButton("Payments", callback_data="payments")],
            [InlineKeyboardButton("Transfer Ownership", callback_data="transfer"),
             InlineKeyboardButton("Delete Bot", callback_data="delete_bot")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Here it is: forrest @yf_test_bot.\nWhat do you want to do with the bot?",
            reply_markup=reply_markup
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("delete", delete_message))
    app.add_handler(CommandHandler("file", send_file))
    app.add_handler(CommandHandler("photo", send_photo))
    app.add_handler(CallbackQueryHandler(button_callback))  # 버튼 클릭 핸들러
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    
    print("봇 시작중...")
    app.run_polling()

if __name__ == '__main__':
    main()