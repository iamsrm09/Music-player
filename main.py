import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Gaane ka naam bhejo, mai MP3 bhej dunga!")

async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if not query or query.startswith('/'):
        return
    
    status = await update.message.reply_text(f"🔍 Searching: {query}...")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            file_name = ydl.prepare_filename(info['entries'][0]).rsplit('.', 1)[0] + ".mp3"
        
        await status.edit_text("📤 Bhej raha hu...")
        await update.message.reply_audio(audio=open(file_name, 'rb'), title=query)
        os.remove(file_name)
        await status.delete()
    except Exception as e:
        await status.edit_text(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_song))
    app.run_polling()

if __name__ == "__main__":
    main()
