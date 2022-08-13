import json
import os

Message = "json/Messages.json"
Channel = "json/Channels.json"
Group = "json/Pathways_Group.json"
Pathway = "json/Sequence.json"
Color = "json/Colors.json"
Levels = "json/Level.json"


def load_Color():
    with open(Color, "r") as f:
        colors = json.load(f)
        colorlist =[]
        for path,color in colors.items():
            for x,oneColor in color.items():
                if x == "s":
                    colorlist.append(oneColor)
                print(f'<p style="background-color:#{oneColor};">{path.split(":")[1]} ({x})</p>')
        return colorlist


def load_Messages():
    if os.path.exists(Message):
        with open(Message, "r") as f:
            return json.load(f)
    else:
        with open(Message, "w") as f:
            dummy = {}
            json.dump(dummy, f, indent=4, separators=(',', ': '), sort_keys=True)
        with open(Message, "r") as f:
            return json.load(f)


def save_Message(users):
    with open(Message, "w") as f:
        json.dump(users, f, indent=4, separators=(',', ': '), sort_keys=True)


def load_Channels():
    if os.path.exists(Channel):
        with open(Channel, "r") as f0:
            return json.load(f0)
    else:
        with open(Channel, "w") as f1:
            dummy = {}
            json.dump(dummy, f1, indent=4, separators=(',', ': '), sort_keys=True)
        with open(Channel, "r") as f2:
            return json.load(f2)


def save_Channels(arg):
    with open(Channel, "w") as f:
        json.dump(arg, f, indent=4, separators=(',', ': '), sort_keys=True)

# todo need the correct file
def load_Pathway():
    pathlist = []
    with open(Group, 'r') as f:
        pathways = json.load(f)

    for name, group in pathways.items():
        for x, path in group.items():
            pathlist.append(f"{path.split(':')[1]}")
    return pathlist


def save_Pathway(Path):
    with open(Pathway, "w") as f:
        json.dump(Path, f, indent=4, separators=(',', ': '), sort_keys=True)


def load_Pathway_group():
        grouplist = []
        with open(Group, 'r') as f:
            pathways = json.load(f)

        for name, group in pathways.items():
                grouplist.append(f"{name}")
        return grouplist


def save_Pathway_group(Path):
    with open(Group, "w") as f:
        json.dump(Path, f, indent=4, separators=(',', ': '), sort_keys=True)


def load_Level():
    if os.path.exists(Levels):
        with open(Levels, "r") as f:
            return json.load(f)
    else:
        with open(Levels, "w") as f:
            dummy = {}
            json.dump(dummy, f, indent=4, separators=(',', ': '), sort_keys=True)
        with open(Levels, "r") as f:
            return json.load(f)


def save_Level(users):
    with open(Levels, "w") as f:
        json.dump(users, f, indent=4, separators=(',', ': '), sort_keys=True)



