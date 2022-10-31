from datetime import date

title_line = -1
description_line = -1
description_end = -1
keywords_line = -1

oVarFile = open("/opt/src/current_values.var", "r")
oVarLines = oVarFile.readlines()
oVarFile.close()

for oVarLine in oVarLines:
    if oVarLine[0:oVarLine.index("=")] == "TITLE":
        read_title = oVarLine[(oVarLine.index("=") + 2):(oVarLine.index("\n") - 1)]
    if oVarLine[0:oVarLine.index("=")] == "DESCRIPTION":
        read_description = oVarLine[(oVarLine.index("=") + 2):(oVarLine.index("\n") - 1)]
    if oVarLine[0:oVarLine.index("=")] == "KEYWORDS":
        read_keywords = oVarLine[(oVarLine.index("=") + 2):(oVarLine.index("\n") - 1)]

count = 0

try:
    ifile = open("/opt/shared/channel_data/description.txt")
    lines = ifile.readlines()
    ifile.close()


    for line in lines:
        count += 1
        try:
            if line[0:line.index(":")] == "TITLE":
                title_line = count
            if line[0:line.index(":")] == "DESCRIPTION":
                description_line = count
            if line[0:line.index(":")] == "KEYWORDS":
                keywords_line = count
        except:
            pass
except:
    pass

if keywords_line != -1:
    description_end = keywords_line - 1
else:
    description_end = count

if title_line != -1:
    title = lines[title_line]
else:
    title = read_title

if description_line != -1:
    description = ""
    for i in range(description_line, description_end):
        description += lines[i]
else:
    description = read_description
    description = description.replace("\\\\", "\\")

if keywords_line != -1:
    keywords = lines[keywords_line]
else:
    keywords = read_keywords

description = description.replace("\\n", "\n")
# description = description.replace("\\\n", "\n")

carrot_count = 0

tmps = title + "\n" + description

for letter in tmps:
    if letter == "<":
        carrot_count += 1

carrot_words = []

tmpstr = tmps
for i in range(0, carrot_count):
    tmpstr = tmpstr[tmpstr.index("<"):len(tmpstr)]
    wordinside = tmpstr[0:(tmpstr.index(">") + 1)]
    carrot_words.append(wordinside)
    tmpstr = tmpstr[(tmpstr.index(">") + 1):len(tmpstr)]

temp_words = []
for theword in carrot_words:
    cutword = theword[1:len(theword)]
    cutword = cutword[0:(len(cutword)-1)]
    temp_words.append(cutword)

varFile = open("/opt/src/current_values.var", "r")
variable_lines = varFile.readlines()
varFile.close()

today = date.today()
today = today.strftime("%b %d %Y")

try:
    timestamps_file = open("/opt/src/timestamps.txt", "r")
    timestamps_lines = timestamps_file.readlines()
    timestamps_file.close()
    timestamps = ""
    for timestamps_line in timestamps_lines:
        timestamps += timestamps_line
except:
    timestamps = "COMING SOON\n"

try:
    otherchannels_file = open("/opt/shared/channel_data/other_channels.txt", "r")
    otherchannels_lines = otherchannels_file.readlines()
    otherchannels_file.close()
    otherchannels = ""
    for otherchannels_line in otherchannels_lines:
        otherchannels += otherchannels_line + "\n"
except:
    otherchannels = "COMING SOON\n"

for theword in temp_words:
    for variable in variable_lines:
        if variable[0:variable.index("=")] == theword:
            tmps = tmps.replace("<" + theword + ">", variable[(variable.index("=") + 1):variable.index("\n")])
    if theword == "VIDEO_TAGS":
        tmps = tmps.replace("<VIDEO_TAGS>", keywords)
    elif theword == "CHANNEL_LIST":
        tmps = tmps.replace("<CHANNEL_LIST>", otherchannels)
    elif theword == "CREATION_DATE":
        tmps = tmps.replace("<CREATION_DATE>", today)
    elif theword == "TIMESTAMPS":
        tmps = tmps.replace("<TIMESTAMPS>", timestamps)
    else:
        tmps = tmps.replace("<" + theword + ">", "")


title = tmps[0:(tmps.index("\n"))]


description = tmps[(tmps.index("\n") + 1):len(tmps)]
# description = description[1:len(description)]
description = description[0:len(description)]


ofile = open("/opt/src/upload_description.txt", "w")
ofile.write(description)
ofile.close()

tfile = open("/opt/src/upload_title.txt", "w")
tfile.write(title)
tfile.close()

ofile = open("/opt/src/upload_keywords.txt", "w")
ofile.write(keywords)
ofile.close()