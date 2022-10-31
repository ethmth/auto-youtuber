varFile = open("/opt/src/current_values.var", "r")
lines = varFile.readlines()
varFile.close()

subreddits_comb = ""
counts_comb = ""

for line in lines:
    if line[0:line.index("=")] == "SUBREDDIT":
        subreddits_comb = line[(line.index("=") + 2):(line.index("\n") - 1)]
    if line[0:line.index("=")] == "COUNT":
        counts_comb = line[(line.index("=") + 2):(line.index("\n") - 1)]

subreddits = subreddits_comb.split(',')

if counts_comb != "":
    counts = counts_comb.split(',')
else:
    counts = ["20"]


oFile = open("/opt/src/subreddits.var", "w")

for subreddit in subreddits:
    oFile.write(subreddit + "\n")

oFile.close()


if len(subreddits) > len(counts):
    diff = len(subreddits) - len(counts)
    for i in range(0,diff):
        counts.append(counts[0])

if len(counts) > len(subreddits):
    diff = len(counts) - len(subreddits)
    for i in range(0,diff):
        counts.pop()


oFile = open("/opt/src/counts.var", "w")

for count in counts:
    oFile.write(count + "\n")

oFile.close()