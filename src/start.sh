#!/bin/bash

mkdir /opt/shared/old/
mv /opt/shared/*.log /opt/shared/old/

START_DATE=$(date +"%Y%m%d_%T")

touch /opt/shared/${START_DATE}.log

SUBREDDIT=${1}
CLIENT_ID=${2}
CLIENT_SECRET=${3}
FREQUENCY=${4}
COUNT=${5}
TITLE=${6}
DESCRIPTION=${7}
KEYWORDS=${8}
CATEGORY=${9}
PRIVACY_STATUS=${10}
BLUR_BACKGROUND=${11}
TIME_OF_DAY=${12}
DAY_OF_WEEK=${13}
DAY_OF_MONTH=${14}
IFTTT_KEY=${15}
IFTTT_EVENT=${16}

echo "START_DATE='${START_DATE}'" > /opt/src/initial_values.var
echo "SUBREDDIT='${SUBREDDIT}'" >> /opt/src/initial_values.var
echo "CLIENT_ID='${CLIENT_ID}'" >> /opt/src/initial_values.var
echo "CLIENT_SECRET='${CLIENT_SECRET}'" >> /opt/src/initial_values.var
echo "FREQUENCY='${FREQUENCY}'" >> /opt/src/initial_values.var
echo "COUNT='${COUNT}'" >> /opt/src/initial_values.var
echo "TITLE='${TITLE}'" >> /opt/src/initial_values.var
echo "DESCRIPTION='${DESCRIPTION}'" >> /opt/src/initial_values.var
echo "KEYWORDS='${KEYWORDS}'" >> /opt/src/initial_values.var
echo "CATEGORY='${CATEGORY}'" >> /opt/src/initial_values.var
echo "PRIVACY_STATUS='${PRIVACY_STATUS}'" >> /opt/src/initial_values.var
echo "BLUR_BACKGROUND='${BLUR_BACKGROUND}'" >> /opt/src/initial_values.var
echo "IFTTT_KEY='${IFTTT_KEY}'" >> /opt/src/initial_values.var
echo "IFTTT_EVENT='${IFTTT_EVENT}'" >> /opt/src/initial_values.var

cp /opt/src/initial_values.var /opt/src/current_values.var

if [[ "$FREQUENCY" == "day" ]]; then
    # CRON_OPEN="*/1 * * * *"
    CRON_OPEN="0 ${TIME_OF_DAY} * * *"
elif [[ "$FREQUENCY" == "week" ]]; then
    CRON_OPEN="0 ${TIME_OF_DAY} * * ${DAY_OF_WEEK}"
elif [[ "$FREQUENCY" == "month" ]]; then
    CRON_OPEN="0 ${TIME_OF_DAY} ${DAY_OF_MONTH} * *"
elif [[ "$FREQUENCY" == "year" ]]; then
    CRON_OPEN="0 ${TIME_OF_DAY} ${DAY_OF_MONTH} * *"
elif [[ "$FREQUENCY" == "all" ]]; then
    # CRON_OPEN="*/10 * * * *"
    CRON_OPEN="0 5 * * *"
else
    CRON_OPEN="*/1 * * * *"
fi

chmod 0744 /opt/src/script.sh
echo "${CRON_OPEN} bash /opt/src/script.sh" > /etc/cron.d/cron-job
chmod 0644 /etc/cron.d/cron-job

crontab /etc/cron.d/cron-job

cron -f

exit 1