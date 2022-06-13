import os
from apiclient.discovery import build
import mysql.connector

import get_stats

def main():
  # Init YouTube Data API client
  GOOGLE_API_KEY = os.getenv("YTSA_GOOGLE_API_KEY")
  if GOOGLE_API_KEY == "":
    raise ValueError("YTSA_GOOGLE_API_KEY is not set.")

  youtube = build(
    'youtube',
    'v3',
    developerKey=GOOGLE_API_KEY
  )
  print("Initialized YouTube Data API client.")

  # Init MySQL connection
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

  # Get parameters from env
  ## Channels parameters
  CHANNELS_FOR_USERNAME = os.getenv("YTSA_CHANNELS_FOR_USERNAME")
  CHANNELS_ID = os.getenv("YTSA_CHANNELS_ID")
  CHANNELS_ID = os.getenv("YTSA_TARGET_CHANNEL_ID") if not CHANNELS_ID else CHANNELS_ID
  CHANNELS_HL = os.getenv("YTSA_CHANNELS_HL")
  ## Videos parameters
  VIDEOS_CHART = os.getenv("YTSA_VIDEOS_CHART")
  VIDEOS_ID = os.getenv("YTSA_VIDEOS_ID")
  VIDEOS_HL = os.getenv("YTSA_VIDEOS_HL")
  VIDEOS_REGION_CODE = os.getenv("YTSA_VIDEOS_REGION_CODE")
  VIDEOS_VIDEO_CATEGORY_ID = os.getenv("YTSA_VIDEOS_VIDEO_CATEGORY_ID")

  # Get stats and record them to the database
  if CHANNELS_FOR_USERNAME or CHANNELS_ID:
    get_stats.get_channels_stats(
      youtube=youtube,
      conn=conn,
      table_prefix=MYSQL_TABLE_PREFIX,
      forUsername=CHANNELS_FOR_USERNAME,
      id=CHANNELS_ID,
      hl=CHANNELS_HL
    )

  if VIDEOS_CHART or VIDEOS_ID:
    get_stats.get_videos_stats(
      youtube=youtube,
      conn=conn,
      table_prefix=MYSQL_TABLE_PREFIX,
      chart=VIDEOS_CHART,
      id=VIDEOS_ID,
      hl=VIDEOS_HL,
      regionCode=VIDEOS_REGION_CODE,
      videoCategoryId=VIDEOS_VIDEO_CATEGORY_ID
    )


  conn.close()


if __name__ == "__main__":
  print("Start main process.")
  main()
  print("Done.")

