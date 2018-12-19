def writeDict(dict, filename, sep):
    with open(filename, "w") as f:
        for i in dict.keys():
            f.write(str(i) + sep + str(dict[i]) + "\n")
