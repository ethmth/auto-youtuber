# Auto-Youtuber

> **NOTE**: The upload.py file was not created by me, but [provided](https://developers.google.com/youtube/v3/guides/uploading_a_video) by YouTube. The rest of the project was written by me.

Uses a combination of Bash and Python to scrape videos from Reddit, combine them into one, then upload them to YouTube. A cronjob within the container does this every 24 hours, or whichever time interval provided, allowing for a fully automated YouTube channel that uploads unique videos daily.

Python scripts are used to create the video descriptions, which contain the titles and timestamps of the original Reddit posts.

> **DISCLAIMER**:
> The author of this program holds no responsibility for what a user may choose to do with the script. I created this as a programming exercise.
> Proceed with caution, keeping YouTube and Reddit's Terms of Service in mind and be aware of potential deterrents that YouTube and/or Reddit may incur if you so choose to use this program irresponsibly.

## Requirements

Requires `docker` and `docker-compose`.

## Setup

### Getting the Files

Ensure `git` is installed, then clone the git repo.

```sh
git clone https://github.com/ethmth/auto-youtuber.git
cd auto-youtuber/
```

### Configuration

Copy the `.env-sample` file and call the copy `.env`.

```sh
cp .env-sample .env
```

Edit the `.env` file based on the examples provided. You will need to create a Google account and configure an OAuth token to upload YouTube videos. More information can be found [here](https://developers.google.com/youtube/v3/guides/uploading_a_video).

```sh
nano .env
```

```
TIME_ZONE=America/New_York
CONTAINER_NAME=yt-reddit-publicfreakout
SUBREDDIT=publicfreakout
CLIENT_ID=96538720639_dummy_youtube_client_id.googleapi.com # Dummy ID
CLIENT_SECRET=583230-86NOT-REAL8632932 # Dummy Secret
FREQUENCY=day
COUNT=10
TITLE=Reddit Public Freakout Compilation | <CREATION_DATE>
DESCRIPTION=Video Created on <CREATION_DATE>\\n\\nThe most epic videos from r/publicfreakout\\n\\nTimestamps:\\n\\n<TIMESTAMPS>
KEYWORDS=Reddit,Youtube
CATEGORY=24
PRIVACY_STATUS=public
BLUR_BACKGROUND=true
TIME_OF_DAY=22
DAY_OF_WEEK=5
DAY_OF_MONTH=30
IFTTT_KEY=6938936893NOTAREALKEY838368383 # Dummy Key
IFTTT_EVENT=youtube
```

`CONTAINER_NAME` is the name of the docker container to be run.

`TIME_ZONE`, `FREQUENCY`, `TIME_OF_DAY`, `DAY_OF_WEEK`, and `DAY_OF_MONTH` specify when and how often you want the container to scrape, create, and upload a video.

`SUBREDDIT` specifies the Subreddit to scrape videos from and `COUNT` specifies how many videos to scrape per video.

`TITLE`, `DESCRIPTION`, `KEYWORDS`,`CATEGORY`, and `PRIVACY_STATUS` refer to attributes of the video to be uploaded. For description formatting, notice that one must use `\\n` to specify a newline, and to insert dynamic values one must use `<>`. `<TIMESTAMPS>`, `<CREATION_DATE>` are two dynamic inserts currently implemented.

`BLUR_BACKGROUND` determines whether the FFmpeg video editor leaves vertical black bars for vertical videos or creates a blurred mosaic effect.

`IFTTT_KEY` and `IFTTT_EVENT` are arguments that allow for IFTTT integration. If a valid webhook key and event are provided, the event will be triggered if YouTube needs you to log in to authenticate an upload.

## Running the Container

While in the repo directory, run the Auto-YouTuber in the background using docker compose.

```sh
docker-compose up -d
```

(Stop the background container by entering the repo directory and running `docker-compose stop`)

The docker container will run, scraping the target Subreddit for videos every so often, depending on the time interval values you provide. It will create a video, then upload it to YouTube. It will repeat this process on the target time on every target time interval until the docker container is stopped.

## Development: Next Steps

- **BUG**: Last timestamp is occasionally cut off from description
- YouTube does not auto-split your video for timestamp intervals shorter than 10 seconds. Make timestamps work for these sections by instating a 10-second minimum interval.
- Improve video quality and resolution using different FFmpeg settings.
- Customize timestamps to include Subreddit, Reddit post title, or both, not just the Reddit post title.
- Make it so one can insert custom clips before, after, or in the middle of a video.
