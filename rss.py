import os
import feedparser
from sql import db
from time import sleep, time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler


api_id = "1782857"   # Get it from my.telegram.org
api_hash = "f222a50cca92872dc48a8e896ffafa8f"   # Get it from my.telegram.org
feed_url = "https://yts.mx/rss"   # RSS Feed URL of the site.
bot_token = "1692419138:AAELm1CMvwiKaw6HbpobTHcL0TTE6Fs02D4"   # Get it by creating a bot on https://t.me/botfather
log_channel = "-1001363921137"   # Telegram Channel ID where the bot is added and have write permission. You can use group ID too.
check_interval = 5   # Check Interval in seconds.  
max_instances = 5   # Max parallel instance to be used.
if os.environ.get("ENV"):   # Add a ENV in Environment Variables if you wanna configure the bot via env vars.
  api_id = os.environ.get("APP_ID")
  api_hash = os.environ.get("API_HASH")
  feed_url = os.environ.get("FEED_URL")
  bot_token = os.environ.get("BOT_TOKEN")
  log_channel = int(os.environ.get("LOG_CHANNEL", None))
  check_interval = int(os.environ.get("INTERVAL", 5))
  max_instances = int(os.environ.get("MAX_INSTANCES", 5))

if db.get_link(feed_url) == None:
  db.update_link(feed_url, "*")

app = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def check_feed():
    FEED = feedparser.parse(feed_url)
    entry = FEED.entries[0]
    if entry.id != db.get_link(feed_url).link:
                   # ↓ Edit this message as your needs.
      message = f"**{entry.title}**\n```{entry.link}```"
      try:
        app.send_message(log_channel, message)
        db.update_link(feed_url, entry.id)
      except FloodWait as e:
        print(f"FloodWait: {e.x} seconds")
        sleep(e.x)
      except Exception as e:
        print(e)
    else:
      print(f"Checked RSS FEED: {entry.id}")



scheduler = BackgroundScheduler()
scheduler.add_job(check_feed, "interval", seconds=check_interval, max_instances=max_instances)
scheduler.start()
app.run()
