import os
import google.auth
import google.auth.transport.requests
import google.auth.transport.urllib3
import google.oauth2.credentials
import googleapiclient.discovery
import pytube

import telebot

# Replace these with your own values
TELEGRAM_API_TOKEN = '5825877289:AAFOoCbe6atF5HGyIPwDTafeAZsZ9PZKvwM'
YOUTUBE_API_KEY = 'AIzaSyDYTPh8Hz-F0yDZR0zO7_ykeT9edD_ew54'

# Initialize the Telegram bot
bot = telebot.TeleBot('5825877289:AAFOoCbe6atF5HGyIPwDTafeAZsZ9PZKvwM', parse_mode=None)

# Set the chat_id of the user or group you want to send the audio to
#cid= (message.chat.id)

@bot.message_handler(commands=['start'])
def start(message):
  
  bot.send_photo(message.chat.id, 'https://imgur.com/a/34qOrh2', caption=f"""🙌 Hello...{message.from_user.full_name} How are you...!!!
  
🙃😎 I am 🎧 #hashtag_musicbot 🎧  


You can  

⬇️ Download Any Song You Want

☢️ Code is Running with Youtube API

💬 Inform Developer About Bugs

⭕️ Coded by @drkvidun

👨🏻‍💻 Just Send the Name of the Song And Wait...""")
  
  #bot.send_message(chat_id, "😊👉🏻 Send the song name You Want: ")

@bot.message_handler(content_types=['text'])
def download_song(message):
  chat_id= (message.chat.id)
  # Use the YouTube API to search for the song
  bot.send_message(chat_id, "Searching The Song... ")
  bot.send_sticker(message.chat.id,sticker="CAACAgIAAxkBAAEBj3pjqLQx69zsDgax4rB8t2srSCovfwAC5QADVp29CggLFmSVBdGKLAQ")
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
  bot.send_message(chat_id, "Song Found... ")#+3
  #bot.delete_message(message.chat.id, message.message_id+1)
  #bot.delete_message(message.chat.id, message.message_id+2)
  

  # Get the first video from the search results
  bot.send_message(chat_id, "Getting File As Video... ")#+4
  #bot.delete_message(message.chat.id, message.message_id+3)
  try:
  # Get the first video from the search results
    video_id = response['items'][0]['id']['videoId']
  except IndexError:
  # Send a message to the user indicating that no results were found
    bot.send_message(chat_id, "Sorry, no results were found for your query.")

  #video_id = response['items'][0]['id']['videoId']
  
  # Download the video as an MP3
  bot.send_message(chat_id, "Downloading File as MP3... ")#+5
  #bot.delete_message(message.chat.id, message.message_id+4)
  yt = pytube.YouTube('https://www.youtube.com/watch?v=' + video_id)
  audio_stream = yt.streams.filter(only_audio=True).first()
  audio_stream.download('./')

  # Get the file path of the downloaded MP3
  file_path = os.path.join('./', audio_stream.default_filename)

  # Send the audio file
  bot.send_message(chat_id, "Sending the Audio File... ")#+6
  #bot.delete_message(message.chat.id, message.message_id+5)
  bot.send_sticker(message.chat.id,sticker="CAACAgIAAxkBAAEBj5pjqLvRCN2zgYJ-Ys7bgyN9i8NE4wACugADMNSdEYTXxIjEUGdWLAQ")
  #bot.delete_message(message.chat.id, message.message_id+6)
  bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'), timeout=3600)
  bot.send_photo(chat_id=chat_id, photo=yt.thumbnail_url)
  bot.send_sticker(message.chat.id,sticker="CAACAgIAAxkBAAEBj4ZjqLbOn_0DUmzynC2szre1g4NKjQAC0wADVp29CvUyj5fVEvk9LAQ")
  os.remove(file_path)
  bot.send_message(chat_id, """ Want to Download More... 😼😽🙀 
  Just Send The Song...😎✌️""")



# Start the bot
bot.polling()
