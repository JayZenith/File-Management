from os import listdir
from os.path import isfile, join


src_dir = "../../Downloads"

onlyfiles = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
for file in onlyfiles:
    print(file)