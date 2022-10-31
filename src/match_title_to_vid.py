import os
import sys
import subprocess
import json
import random

number_of_subs = int(sys.argv[1])

iFile = open("/opt/src/video_links.tmp", "r")
lines = iFile.readlines()
iFile.close()

strFile = open("/opt/src/files_titles.temp", "w")

for line in lines:
    file_name = line[(line.index(".it/") + 4):line.index("\n")]
    real_file_name = subprocess.check_output(f"ls /opt/src/ | grep {file_name}", shell=True)
    real_file_name = str(real_file_name)
    for i in range(0,number_of_subs):
        jsonFile = open(f"/opt/src/subreddit_{i}.json", "r")
        data = json.load(jsonFile)
        jsonFile


        bigdata = data["data"]
        children = bigdata["children"]
        for child in children:
            lildata = child["data"]
            dest_url = lildata["url_overridden_by_dest"]
            dest_url = dest_url[(dest_url.index(".it/") + 4):len(dest_url)]
            if dest_url == file_name:
                title = lildata["title"]
                real_file_name += " '" + title + "'\n"

    strFile.write(real_file_name)

strFile.close()

lines = []

strFile = open("/opt/src/files_titles.temp", "r")
lines = strFile.readlines()
random.shuffle(lines)
strFile.close()

count = 0

orderedTitle = open("/opt/src/orderedTitles.txt", "w")

for line in lines:
    count += 1

    file_name = line[(line.index("b'") + 2):line.index("\\n")]
    title = line[line.index("\\n'") + 5:line.index("'\n")]

    if count < 10:
        count_text = "000" + str(count)
    elif count < 100:
        count_text = "00" + str(count)
    elif count < 1000:
        count_text = "0" + str(count)
    else:
        count_text = str(count)

    os.system(f"mv /opt/src/{file_name} /opt/src/{count_text}.mp4")

    duration = subprocess.check_output(f'mediainfo --Inform="General;%Duration%" {count_text}.mp4', shell=True)
    duration = str(duration)
    orderedTitle.write("'" + title + "' " + duration + "\n")

orderedTitle.close()