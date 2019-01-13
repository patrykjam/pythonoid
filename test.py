from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir("sounds/") if isfile(join("sounds/", f))]

print(onlyfiles)