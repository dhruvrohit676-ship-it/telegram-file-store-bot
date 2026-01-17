from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8411775495:AAFLaFbUwj1Bf_j2u_MremIirGN81yupqFE"
ADMIN_ID = 8199455187  # your telegram user id

files_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        key = context.args[0]
        if key in files_db:
            await context.bot.send_document(update.message.chat_id, files_db[key])
        else:
            await update.message.reply_text("❌ File not found.")
    else:
        await update.message.reply_text("📁 Private File Storage Bot\nSend file to store.")

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not allowed to upload.")
        return

    file = update.message.document or update.message.video
    file_id = file.file_id
    key = str(len(files_db) + 1)
    files_db[key] = file_id

    link = f"https://t.me/{context.bot.username}?start={key}"
    await update.message.reply_text(f"✅ Stored!\n🔗 Link:\n{link}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL, save_file))
app.run_polling()

