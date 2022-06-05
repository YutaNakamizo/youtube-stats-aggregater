#!/bin/sh

# Setup crontab
echo "$YTSA_INTERVAL python $YTSA_APP_DIR/src/main.py" >> /var/spool/cron/crontabs/root

# Launch crontab
crond -f

