from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8411775495:AAFLaFbUwj1Bf_j2u_MremIirGN81yupqFE"
ADMIN_ID = 8199455187  # paste your user id

files_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📁 File Storage Bot\nSend a file to store it.")

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not allowed to upload.")
        return

    file = update.message.document or update.message.video
    file_id = file.file_id
    unique_id = str(len(files_db) + 1)

    files_db[unique_id] = file_id

    link = f"https://t.me/{context.bot.username}?start={unique_id}"
    await update.message.reply_text(f"✅ File stored!\n🔗 Share link:\n{link}")

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return

    file_key = context.args[0]
    if file_key in files_db:
        await context.bot.send_document(update.message.chat_id, files_db[file_key])
    else:
        await update.message.reply_text("❌ File not found.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", get_file))
app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL, save_file))

app.run_polling()
