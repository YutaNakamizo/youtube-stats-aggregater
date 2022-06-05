import os
from datetime import datetime
from apiclient.discovery import build
import mysql.connector

def main():
  # Init YouTube Data API client
  GOOGLE_API_KEY = os.getenv("YTSA_GOOGLE_API_KEY")
  if GOOGLE_API_KEY == "":
    raise ValueError("GOOGLE_API_KEY is not set.")

  youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
  print("Initialized YouTube Data API client.")

  # Get stats via YouTube Data API
  TARGET_CHANNEL_ID = os.getenv("YTSA_TARGET_CHANNEL_ID")
  if TARGET_CHANNEL_ID == "":
    raise ValueError("YTSA_TARGET_CHANNEL_ID is not set.")

  stats_resp = youtube.channels().list(
    part="statistics",
    id=TARGET_CHANNEL_ID
  ).execute()
  print("Executed list action on YouTube Channel for channelId.")

  if not stats_resp["items"]:
    raise IndexError("YouTube Data API returned empty response.")

  stats = stats_resp["items"][0]["statistics"]

  # Init MySQL database and table
  MYSQL_TABLE_PREFIX = os.getenv("YTSA_MYSQL_TABLE_PREFIX")
  tablename = MYSQL_TABLE_PREFIX + "statistics"

  conn = mysql.connector.connect(
    host=os.getenv("YTSA_MYSQL_HOST"),
    port=os.getenv("YTSA_MYSQL_PORT"),
    user=os.getenv("YTSA_MYSQL_USER"),
    password=os.getenv("YTSA_MYSQL_PASSWORD"),
    database=os.getenv("YTSA_MYSQL_DATABASE")
  )
  print("Connected to MySQL server.")

  cur = conn.cursor()

  cur.execute(
    "CREATE TABLE IF NOT EXISTS `" + tablename + "` (" \
    "  id int not null primary key auto_increment," \
    "  datetime datetime not null default current_timestamp," \
    "  channelId tinytext not null," \
    "  subscriberCount int unsigned default null," \
    "  viewCount int unsigned default null," \
    "  videoCount int unsigned default null," \
    "  commentCount int unsigned default null" \
    ");"
  )
  print("Created table on MySQL server (if not exists)")

  # Insert stats into MySQL
  now = datetime.now()
  cur.execute(
    "INSERT INTO" \
    "`" + tablename + "`" \
    "(" \
    "  datetime," \
    "  channelId," \
    "  subscriberCount," \
    "  viewCount," \
    "  videoCount," \
    "  commentCount" \
    ")" \
    "VALUES" \
    "(" \
    "  %(datetime)s," \
    "  %(channelId)s," \
    "  %(subscriberCount)s," \
    "  %(viewCount)s," \
    "  %(videoCount)s," \
    "  %(commentCount)s" \
    ");",
    {
      "datetime": now.strftime('%Y-%m-%d %H:%M:%S.%f'),
      "channelId": TARGET_CHANNEL_ID,
      "subscriberCount": int(stats["subscriberCount"]) if "subscriberCount" in stats else None,
      "viewCount": int(stats["viewCount"]) if "viewCount" in stats else None,
      "videoCount": int(stats["videoCount"]) if "videoCount" in stats else None,
      "commentCount": int(stats["commentCount"]) if "commentCount" in stats else None
    }
  )
  print("Inserted statistics record into MySQL server.")

  cur.close()
  conn.commit()
  print("All transactions are committed.")

  conn.close()


if __name__ == "__main__":
  print("Start main process.")
  main()
  print("Done.")

