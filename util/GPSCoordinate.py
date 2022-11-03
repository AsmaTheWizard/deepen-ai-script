import json
import os
import math
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]

directory=input_path
list=[]
for filename in os.listdir(directory):
    f = open(os.path.join(directory, filename))
    data = json.load(f)
    dictionary={
        "title":directory,
        "timestamp":data["timestamp"],
        "latitude":data["gnss"]["latitude"]*180/math.pi,
        "longitude":data["gnss"]["longitude"]*180/math.pi,
        "altitude":data["gnss"]["altitude"]
    }
    list.append(dictionary)

with open(output_path+"\output.json", "w") as outfile:
    json.dump(list, outfile)
f.close()


