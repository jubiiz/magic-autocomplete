path = "unf_lists/Affinity/0.txt"

with open(path, "r") as r:
    for line in r:
        line = line.rstrip("\n")
        num = line[0:line.find(" ")]
        cardname = line[line.find(" "):]
        print(cardname)