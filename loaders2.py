import json
from pprint import pprint


def load_pathways():
    pathlist = []
    with open(r"D:\LOM\arrodes\json\Pathways_Group.json", 'r') as f:
        pathways = json.load(f)

    for name,group in pathways.items():
        for x,path in group.items():
            pathlist.append(f"{path.split(':')[1]}")
    return pathlist