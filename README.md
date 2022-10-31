# Auto-Youtuber

*NOTE*: The upload.py file was not written by me, but provided by YouTube. The rest of the python scripts were written by me.

*WORK IN PROGRESS*

Intended to be run in a docker container.

This is a very messy project but for the most part it works.

Uses a combination of bash and python to scrape videos from reddit, combine them into one, then upload them to youtube. A cronjob within the container does this every 24 hours, allowing for a fully automated YouTube channel.

I use python scripts to create the video description, which contains the titles and timestamps of the original reddit posts.

Will not work as is outside of a docker container or without a .env file


### Things to Fix
- Last timestamp got cut off
- Make timestamps work for sections (must be 10 seconds between)
- Improve video quality and resolution
- Customize timestamps to include subreddit or title or both
- Make it so I can insert clips before, after, or in the middle of a video (first,last,mid,q1,q2 or specify custom number)

