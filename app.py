import google.auth
import google.auth.transport.requests
import google.auth.transport.urllib3
import google.oauth2.credentials
import googleapiclient.discovery
import pytube
import tempfile
import shutil
import io

import telebot

# Replace these with your own values
TELEGRAM_API_TOKEN = '5825877289:AAGBywxCM0jX7r1P8bcfzG5Eyi2VGhAJnys'
YOUTUBE_API_KEY = 'AIzaSyC00yh-jggAKEhIeeXcvfIxdrNnADAuy20'

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, 'https://imgur.com/a/34qOrh2', caption=f"""🙌 Hello...{message.from_user.full_name} How are you...!!!

🙃😎 I am 🎧 #hashtag_musicbot V.0.1.1 🎧

You can
⬇️ Download Any Song You Want
☢️ Code is Running with Youtube API
💬 Inform Developer About Bugs
⭕️ Coded by @drkvidun
👨🏻‍💻 Just Send the Name of the Song And Wait...""")

@bot.message_handler(content_types=['text'])
def download_song(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "Searching The Song... ")
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEBj3pjqLQx69zsDgax4rB8t2srSCovfwAC5QADVp29CggLFmSVBdGKLAQ")

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part='id',
        type='video',
        q=message.text,
        videoDefinition='high',
        maxResults=1,
        fields='items(id(videoId))'
    )
    response = request.execute()
    bot.send_message(chat_id, "Song Found... ")

    try:
        video_id = response['items'][0]['id']['videoId']
    except IndexError:
        bot.send_message(chat_id, "Sorry, no results were found for your query.")

    bot.send_message(chat_id, "Downloading File as MP3... ")
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEBj5pjqLvRCN2zgYJ-Ys7bgyN9i8NE4wACugADMNSdEYTXxIjEUGdWLAQ")

    # Download the video as an MP3
    yt = pytube.YouTube('https://www.youtube.com/watch?v=' + video_id)
    video_stream = yt.streams.filter(only_audio=True).first()

    with io.BytesIO() as video_bytes:
        video_stream.stream_to_buffer(video_bytes)
        video_bytes.seek(0)

        # Send the audio file
        bot.send_audio(chat_id=chat_id, audio=video_bytes.read(), timeout=3600)

    bot.send_photo(chat_id=chat_id, photo=yt.thumbnail_url)
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEBj4ZjqLbOn_0DUmzynC2szre1g4NKjQAC0wADVp29CvUyj5fVEvk9LAQ")
    bot.send_message(chat_id, """Want to Download More... 😼😽🙀 
Just Send The Song...😎✌️""")

# Start the bot
bot.polling()
