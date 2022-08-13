import json
import sqlite3
from pprint import pprint

from colorsFunc import linear_gradient

Message = "json/Messages.json"
Channel = "json/Channels.json"
Group = "json/Pathways_Group.json"
Pathway = "json/Sequence.json"
Color = r"D:\LOM\arrodes\json\Colors.json"
funny = r"D:\LOM\arrodes\json\pathwaysandgroup.json"
colorlistS = []
colorlistE = []
x = 0
c = 0
conn = sqlite3.connect('../acting_method.db')

with open(funny, 'r') as f:
    fun = json.load(f)
    # print(len(fun))

colorsCursor = conn.execute("SELECT colors_hex,colors_path FROM colors")
pathwaysCursor = conn.execute("SELECT pathways_name FROM pathways")
# print(colors)
# for color,path in colors:
colors = {}
for color, path in colorsCursor:
    colors[path] = color

    # print(f"colors:{paths}}")
    # if paths == path[0]:
    #     print(color)
    # for types, hexa in color.items():
    #     if types == "s":
    #         colorlistS.append(hexa)
    #     elif types == "e":
    #         colorlistE.append(hexa)

for group, pathways in fun.items():
    for pathN in pathways:
        for num, seq in pathN.items():
            x += 1
            grad = linear_gradient(colors[pathN['0']], "e6e6e6", 11)['hex'][int(num)]
            updateQuery = (f"UPDATE sequences SET sequences_color = '{grad}' WHERE sequences_name == '{seq}';")
            conn.execute(updateQuery)
            insertQuery = (f"INSERT INTO "
                           f"sequences("
                           f"sequences_id,"
                           f"sequences_num,"
                           f"sequences_name,"
                           f"sequences_pathway,"
                           f"sequences_color,"
                           f"sequences_group) "
                           f"VALUES({x},{num},'{seq}','{pathN['0']}','{grad}','{group}');")
            conn.commit()

# print(int(((int(num)+1)*(int(num)+1))))
# print(linear_gradient(colorlistS[c - 1], colorlistE[c - 1],50)["hex"][int(num)])

# print(f'<p style="background-color:#{grad};">{pathN["0"]}-{seq}</p>')
