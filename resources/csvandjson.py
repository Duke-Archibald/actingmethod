import collections
import csv

import json
import sqlite3

from resources.colorsFunc import linear_gradient
conn = sqlite3.connect('../resources/acting_method.db')


def data_seq_to_csv():
    sequenceListCursor = conn.execute(f"SELECT "
                                      f"sequences_num,"
                                      f"sequences_name,"
                                      f"sequences_pathway,"
                                      f"sequences_color,"
                                      f"sequences_group"
                                      f" FROM sequences")
    csvList = "Group,Pathway,Sequence_name,Sequence_num,Sequence_color\n"
    for num, name, path, color, group in sequenceListCursor:
        csvList += f"{group},{path},{name},{num},{color}\n"

    with open("pathwaylist.csv", "w") as file:
        file.write(csvList)


def data_color_to_dict():
    colorsCursor = conn.execute(f"SELECT colors_hex,colors_path FROM colors")
    colors = {}
    for color, path in colorsCursor:
        colors[path] = color
    return colors


def new_path_color():
    x = 0
    with open("./pathwaysandcolor.json", "r") as file:
        jsondict = json.load(file)
        for group in jsondict:
            # print(group)
            for path in jsondict[group]:
                # print("\t"+path)
                for seq in jsondict[group][path]:
                    # print("\t\t"+seq)
                    seqNum = [val for val in jsondict[group][path][seq].values()]
                    x += 1
                    grad = linear_gradient(data_color_to_dict()[path], "e6e6e6", 11)['hex'][int(seqNum[0])]
                    print(x)
                    print(seqNum[0])
                    print(seq)
                    print(path)
                    print(grad)
                    print(group)
                    print()
                    updateQuery = (f"UPDATE sequences SET sequences_color = '{grad}' WHERE sequences_name == '{seq}';")
                    conn.execute(updateQuery)
            #       insertQuery = (f"INSERT INTO "
            #                f"sequences("
            #                f"sequences_id,"
            #                f"sequences_num,"
            #                f"sequences_name,"
            #                f"sequences_pathway,"
            #                f"sequences_color,"
            #                f"sequences_group) "
            #                f"VALUES({x},{num},'{seq}','{pathN['0']}','{grad}','{group}');")
                    conn.commit()


def nesteddict():
    return collections.defaultdict(nesteddict)


def to_json():
    Group, Pathway, Sequence_name, Sequence_num, Sequence_color = \
        "Group", "Pathway", "Sequence_name", "Sequence_num", "Sequence_color"
    new_data_dict = nesteddict()
    with open("pathwaylist.csv", "r") as data_file:
        data = csv.DictReader(data_file, delimiter=",")
        for row in data:
            new_data_dict[row[Group]][row[Pathway]][row[Sequence_name]] = {Sequence_num: row[Sequence_num],
                                                                           Sequence_color: row[Sequence_color]}

        # dump as textData to have a clean, indented representation

    with open("pathwaysandcolor.json", "w") as file:
        file.write(json.dumps(new_data_dict, indent=2))

data_seq_to_csv()
to_json()