FROM debian:11.4

ARG TIME_ZONE
ENV time=${TIME_ZONE}

RUN apt update && apt upgrade -y && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/${time} /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt install python3 ffmpeg python3-pip curl youtube-dl jq mediainfo cron firefox-esr git -y

# INSTALL PYTHON 2
# RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py 
# RUN python2 get-pip.py
# RUN python2 -m pip install --upgrade google-api-python-client oauth2client httplib2

RUN python3 -m pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 oauth2client datetime selenium

# INSTALL GECKODRIVER FOR USE WITH SELENIUM
# RUN cd /tmp
# RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
# RUN tar -xvf geckodriver-v0.31.0-linux64.tar.gz
# RUN mv geckodriver /usr/local/bin
# RUN chmod +x /usr/local/bin/geckodriver

COPY ./src /opt/src

WORKDIR /opt/src/

RUN chmod +x /opt/src/start.sh

ENTRYPOINT ["/opt/src/start.sh"]
CMD [""]