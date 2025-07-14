import logging
from aiogram import Bot, Dispatcher, executor, types
import subprocess
import os

API_TOKEN = '7647515503:AAGS7t15F-BC-JewX6EcnpuBK2z-YOYGwP8'  # <-- Replace this with your actual token from @BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def welcome_message(message: types.Message):
    await message.reply(
        "👋 Welcome to Insta Downloader Bot!\n\n"
        "📥 Send me any *Instagram reel/video/post link* and I will send you the video.\n\n"
        "⚠️ Make sure the link is public.\n\n"
        "💬 Credit: @ritikxyz099",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: "instagram.com" in message.text)
async def download_instagram_video(message: types.Message):
    url = message.text.strip()
    await message.reply("📥 Downloading video... please wait...")

    try:
        filename = "insta_video.%(ext)s"
        command = [
            "yt-dlp",
            "-f", "mp4",
            "-o", filename,
            url
        ]
        subprocess.run(command, check=True)

        downloaded_file = None
        for file in os.listdir():
            if file.startswith("insta_video") and file.endswith(".mp4"):
                downloaded_file = file
                break

        if downloaded_file:
            with open(downloaded_file, 'rb') as video:
                await message.reply_video(video, caption="✅ Here is your video\n\nCredit: @ritikxyz099")
            os.remove(downloaded_file)
        else:
            await message.reply("❌ Video not found after download.")

    except Exception as e:
        await message.reply(f"❌ Error occurred: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
