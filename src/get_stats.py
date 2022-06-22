from datetime import datetime

# youtube: YouTube Data API Client object
# conn: MySQL connection object
# table_prefix: MySQL table name prefix
# (rest of args): YouTube Data API parameters
def get_channels_stats(youtube, forUsername, id, hl, conn, table_prefix):
  hl = None if not hl else hl

  # Validate parameters
  if(
    (not forUsername and not id)
    or (forUsername and id)
  ):
    raise ValueError("Specify exactly one of chart or id")
  
  # Get stats via YouTube Data API
  now = datetime.now()
  now_str = now.strftime('%Y-%m-%d %H:%M:%S.%f')

  stats_all = []
  
  stats_req = None

  if forUsername:
    stats_req = youtube.channels().list(
      part="id,statistics",
      forUsername=forUsername,
      hl=hl,
      maxResults=50
    )
  elif id:
    stats_req = youtube.channels().list(
      part="id,statistics",
      id=id,
      hl=hl,
      maxResults=50
    )

  stats_res = stats_req.execute()
  stats_all.extend(stats_res["items"])

  while True:
    stats_res = youtube.channels().list_next(stats_req, stats_res)
    if stats_res == None:
      break
    stats_all.extend(stats_res["items"])

  print("Executed list action on YouTube Channel(s).")

  # Init MySQL database and table
  cur = conn.cursor()
  
  table_name = table_prefix + "channels"
  print(table_name)
  cur.execute(
    "CREATE TABLE IF NOT EXISTS `" + table_name + "` (" \
    "  id int not null primary key auto_increment," \
    "  datetime datetime not null default current_timestamp," \
    "  channelId tinytext not null," \
    "  subscriberCount int unsigned default null," \
    "  viewCount int unsigned default null," \
    "  videoCount int unsigned default null," \
    "  commentCount int unsigned default null" \
    ");"
  )
  print("Created channels table on MySQL server (if not exists)")

  # Insert stats into MySQL
  def convert_ytitem_to_sqlrecord(item):
    id = item["id"]
    stats = item["statistics"]
    return {
      "datetime": now_str,
      "channelId": id,
      "subscriberCount": int(stats["subscriberCount"]) if "subscriberCount" in stats else None,
      "viewCount": int(stats["viewCount"]) if "viewCount" in stats else None,
      "videoCount": int(stats["videoCount"]) if "videoCount" in stats else None,
      "commentCount": int(stats["commentCount"]) if "commentCount" in stats else None
    }

  records = list(map(
    convert_ytitem_to_sqlrecord,
    stats_all
  ))

  cur.executemany(
    "INSERT INTO" \
    "`" + table_name + "`" \
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
    records
  )
  print("Inserted channels stats record(s) into MySQL server.")

  cur.close()
  conn.commit()

  print("Channels transactions are committed.")


# youtube: YouTube Data API Client object
# conn: MySQL connection object
# (rest of args): YouTube Data API parameters
def get_videos_stats(youtube, chart, id, hl, regionCode, videoCategoryId, conn, table_prefix):
  hl = None if not hl else hl
  regionCode = None if not regionCode else regionCode
  videoCategoryId = None if not videoCategoryId else videoCategoryId

  # Validate parameters
  if(
    (not chart and not id)
    or (chart and id)
  ):
    raise ValueError("Specify exactly one of chart or id")
  
  # Get stats via YouTube Data API
  now = datetime.now()
  now_str = now.strftime('%Y-%m-%d %H:%M:%S.%f')

  stats_all = []
  
  stats_req = None

  if chart:
    stats_req = youtube.videos().list(
      part="id,statistics",
      chart=chart,
      hl=hl,
      regionCode=regionCode,
      videoCategoryId=videoCategoryId,
      maxResults=50
    )
  elif id:
    stats_req = youtube.videos().list(
      part="id,statistics",
      id=id,
      hl=hl,
      regionCode=regionCode,
      videoCategoryId=videoCategoryId,
      maxResults=50
    )

  stats_res = stats_req.execute()
  stats_all.extend(stats_res["items"])

  while True:
    stats_res = youtube.videos().list_next(stats_req, stats_res)
    if stats_res == None:
      break
    stats_all.extend(stats_res["items"])

  print("Executed list action on YouTube Video(s).")

  # Init MySQL database and table
  cur = conn.cursor()
  
  table_name = table_prefix + "videos"
  cur.execute(
    "CREATE TABLE IF NOT EXISTS `" + table_name + "` (" \
    "  id int not null primary key auto_increment," \
    "  datetime datetime not null default current_timestamp," \
    "  videoId tinytext not null," \
    "  viewCount int unsigned default null," \
    "  likeCount int unsigned default null," \
    "  dislikeCount int unsigned default null," \
    "  favoriteCount int unsigned default null," \
    "  commentCount int unsigned default null" \
    ");"
  )
  print("Created videos table on MySQL server (if not exists)")

  # Insert stats into MySQL
  def convert_ytitem_to_sqlrecord(item):
    id = item["id"]
    stats = item["statistics"]
    return {
      "datetime": now_str,
      "videoId": id,
      "viewCount": int(stats["viewCount"]) if "viewCount" in stats else None,
      "likeCount": int(stats["likeCount"]) if "likeCount" in stats else None,
      "dislikeCount": int(stats["dislikeCount"]) if "dislikeCount" in stats else None,
      "favoriteCount": int(stats["favoriteCount"]) if "favoriteCount" in stats else None,
      "commentCount": int(stats["commentCount"]) if "commentCount" in stats else None
    }

  records = list(map(
    convert_ytitem_to_sqlrecord,
    stats_all
  ))

  cur.executemany(
    "INSERT INTO" \
    "`" + table_name + "`" \
    "(" \
    "  datetime," \
    "  videoId," \
    "  viewCount," \
    "  likeCount," \
    "  dislikeCount," \
    "  favoriteCount," \
    "  commentCount" \
    ")" \
    "VALUES" \
    "(" \
    "  %(datetime)s," \
    "  %(videoId)s," \
    "  %(viewCount)s," \
    "  %(likeCount)s," \
    "  %(dislikeCount)s," \
    "  %(favoriteCount)s," \
    "  %(commentCount)s" \
    ");",
    records
  )
  print("Inserted videos stats record(s) into MySQL server.")

  cur.close()
  conn.commit()

  print("Videos transactions are committed.")

