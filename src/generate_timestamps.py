ifile = open("/opt/src/orderedTitles.txt", "r")
lines = ifile.readlines()
ifile.close()

total_time = 0

ofile = open("/opt/src/timestamps.txt", "w")

for line in lines:
    temp = line[(line.index("'") + 1):(line.index("\n"))]
    title = temp[0:temp.index("'")]
    temp = temp[(temp.index("'") + 1):len(temp)]
    temp = temp[(temp.index("'") + 1):len(temp)]
    duration = temp[0:temp.index("\\n'")]
    duration = int(duration)

    mins = int(total_time) // int(60000)
    secs = (int(total_time) % int(60000)) // int(1000)
    mins = str(mins)
    secs = str(secs)
    if len(mins) == 1:
        mins = "0" + mins
    if len(secs) == 1:
        secs = "0" + secs
    time_stamp = str(mins) + ":" + str(secs)

    ofile.write(time_stamp + "  \t" + title + "\n")

    total_time += duration

ofile.close()