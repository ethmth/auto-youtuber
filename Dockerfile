FROM debian:11.4

ARG TIME_ZONE
ENV time=${TIME_ZONE}

RUN apt update && apt upgrade -y && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/${time} /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt install python3 ffmpeg python3-pip curl youtube-dl jq mediainfo cron firefox-esr git -y

RUN python3 -m pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 oauth2client datetime selenium

COPY ./src /opt/src

WORKDIR /opt/src/

RUN chmod +x /opt/src/start.sh

ENTRYPOINT ["/opt/src/start.sh"]
CMD [""]