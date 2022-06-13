# youtube-stats-aggregater
A Python script to collect and aggregate stats of YouTube contents with Docker.

## Environments

### Pooling Config
You can set `YTSA_INTERVAL`, a crontab interval string with 5 sections.  
Default value is `"*/5 * * * *"` (Every 5 minutes)

#### Channels
See [Channels: list  |  YouTube Data API  |  Google Developers](https://developers.google.com/youtube/v3/docs/channels/list).

- `YTSA_CHANNELS_FOR_USERNAME`: forUsername filter
- `YTSA_CHANNELS_ID`: id filter
- `YTSA_CHANNELS_HL`: hl parameter

#### Videos
See [Videos: list  |  YouTube Data API  |  Google Developers](https://developers.google.com/youtube/v3/docs/videos/list).

- `YTSA_VIDEOS_CHART`: chart filter
- `YTSA_VIDEOS_ID`: id filter
- `YTSA_VIDEOS_HL`: hl parameter
- `YTSA_VIDEOS_REGION_CODE`: regionCode: parameter
- `YTSA_VIDEOS_VIDEO_CATEGORY_ID`: videoCategoryId parameter

### GCP Project Config
Set `YTSA_GOOGLE_API_KEY`, anAPI key of Google Cloud Platform Project which is enabled YouTube Data API v3.

### MySQL Config
Set MySQL connection config (hostname, port, username, password and database) to `YTSA_MYSQL_HOST`, `YTSA_MYSQL_PORT`, `YTSA_MYSQL_USER`, `YTSA_MYSQL_PASSWORD` and `YTSA_MYSQL_DATABASE`.  
Default value of `YTSA_MYSQL_PORT` is `"3306"`, and of `YTSA_MYSQL_DATABASE` is `"ytsa"`.

Before you run the container, you need to create a database and a user which have at least create and insert access to the database.

You can also set `YTSA_MYSQL_TABLE_PREFIX`, a prefix of table name which the contaier creates and use to store records.  
Default value is `"ytsa_"`.

