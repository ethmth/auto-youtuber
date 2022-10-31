#!/bin/bash

source "/opt/src/current_values.var"
source "/opt/shared/client_data/variables.var" || echo ""

CURRENT_DATE=$(date +"%Y%m%d_%T")
echo "${CURRENT_DATE} script.sh Starting Script" >> /opt/shared/${START_DATE}.log

echo "START_DATE='${START_DATE}'" > /opt/src/current_values.var
echo "SUBREDDIT='${SUBREDDIT}'" >> /opt/src/current_values.var
echo "CLIENT_ID='${CLIENT_ID}'" >> /opt/src/current_values.var
echo "CLIENT_SECRET='${CLIENT_SECRET}'" >> /opt/src/current_values.var
echo "FREQUENCY='${FREQUENCY}'" >> /opt/src/current_values.var
echo "COUNT='${COUNT}'" >> /opt/src/current_values.var
echo "TITLE='${TITLE}'" >> /opt/src/current_values.var
echo "DESCRIPTION='${DESCRIPTION}'" >> /opt/src/current_values.var
echo "KEYWORDS='${KEYWORDS}'" >> /opt/src/current_values.var
echo "CATEGORY='${CATEGORY}'" >> /opt/src/current_values.var
echo "PRIVACY_STATUS='${PRIVACY_STATUS}'" >> /opt/src/current_values.var
echo "BLUR_BACKGROUND='${BLUR_BACKGROUND}'" >> /opt/src/current_values.var
echo "IFTTT_KEY='${IFTTT_KEY}'" >> /opt/src/current_values.var
echo "IFTTT_EVENT='${IFTTT_EVENT}'" >> /opt/src/current_values.var

python3 /opt/src/update_client_secrets.py
python3 /opt/src/process_multiple_subs.py

cd /opt/src/
mkdir outvids

readarray -t SUBREDDITS < <(cat /opt/src/subreddits.var)
readarray -t COUNTS < <(cat /opt/src/counts.var)

CURRENT_DATE=$(date +"%Y%m%d_%T")
echo "${CURRENT_DATE} script.sh Starting Video Downloads" >> /opt/shared/${START_DATE}.log

for (( i=0; i<${#SUBREDDITS[@]}; i++ ))
do
    :
    (curl -s -H "User-agent: 'bot 0.1'" https://www.reddit.com/r/${SUBREDDITS[i]}/top/.json\?t=${FREQUENCY}\&limit=${COUNTS[i]} | jq '.' > /opt/src/subreddit_${i}.json)

    (cat subreddit_${i}.json | grep url_overridden_by_dest | grep -Eoh "https:\/\/v\.redd\.it/\w{13}") >> /opt/src/video_links.tmp
done

youtube-dl $(cat /opt/src/video_links.tmp)

python3 /opt/src/match_title_to_vid.py ${#SUBREDDITS[@]}
python3 /opt/src/generate_timestamps.py
python3 /opt/src/overwrite_description.py

CURRENT_DATE=$(date +"%Y%m%d_%T")
echo "${CURRENT_DATE} script.sh Starting Video Blurring/Moving" >> /opt/shared/${START_DATE}.log

if [[ "$BLUR_BACKGROUND" == "true" ]]; then
    for f in *.mp4;
    do
        echo $f
        ffmpeg -i $f -lavfi '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16' -vb 800K outvids/$f ;
    done
else
    mv *.mp4 outvids/
fi

rm *.mp4
for f in outvids/*.mp4; do echo "file $f" >> file_list.txt; done


CURRENT_DATE=$(date +"%Y%m%d_%T")
echo "${CURRENT_DATE} script.sh Concatinating Videos into One" >> /opt/shared/${START_DATE}.log

ffmpeg -f concat -i file_list.txt final.mp4
rm -rf outvids

UPLOAD_TITLE=$(cat /opt/src/upload_title.txt)
UPLOAD_DESCRIPTION=$(cat /opt/src/upload_description.txt)
UPLOAD_KEYWORDS=$(cat /opt/src/upload_keywords.txt)

CURRENT_DATE=$(date +"%Y%m%d_%T")
echo "${CURRENT_DATE} script.sh Starting Upload Script" >> /opt/shared/${START_DATE}.log

cp /opt/shared/client_data/upload.py-oauth2.json /opt/src/upload.py-oauth2.json || echo ""
python3 -u /opt/src/upload.py --file="/opt/src/final.mp4" --title="${UPLOAD_TITLE}" --description="${UPLOAD_DESCRIPTION}" --keywords="${UPLOAD_KEYWORDS}" --category="${CATEGORY}" --privacyStatus="${PRIVACY_STATUS}" | tee /opt/src/pyout.txt
cp /opt/src/upload.py-oauth2.json /opt/shared/client_data/upload.py-oauth2.json || echo ""


CURRENT_DATE=$(date +"%Y%m%d_%T")
echo "${CURRENT_DATE} script.sh After Script" >> /opt/shared/${START_DATE}.log
echo " " >> /opt/shared/${START_DATE}.log

exit 0