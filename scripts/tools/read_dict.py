def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            key, value = line.split(sep)
            dict.update({key: value[:-1]})
        return dict