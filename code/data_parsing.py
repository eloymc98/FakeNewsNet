import json
import os

ids_dict = {}  # dictionary to compress the data

def parsing_followers():

    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_followers'):
        fileList.append(filenames)

    for file in fileList[0][2]:
        filename = 'fakenewsnet_dataset/user_followers/{}'.format(file)
        json_object = json.load(open(filename))

        id = json_object["user_id"]
        if len(ids_dict) == 0:
            ids_dict[id] = 1
        if id not in ids_dict.keys():
            max_value = max(ids_dict.values())
            ids_dict[id] = max_value + 1
        followers = json_object["followers"]

        with open('graph.txt', 'a+') as f:
            for user in followers:
                if user not in ids_dict.keys():
                    max_value = max(ids_dict.values())
                    ids_dict[user] = max_value+1
                f.write(str(ids_dict[id]) + " " + str(ids_dict[user]) + "\n")


def parsing_following():
    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_following'):
        fileList.append(filenames)

    for file in fileList[0][2]:
        filename = 'fakenewsnet_dataset/user_following/{}'.format(file)
        json_object = json.load(open(filename))

        id = json_object["user_id"]
        if len(ids_dict) == 0:
            ids_dict[id] = 1
        if id not in ids_dict.keys():
            max_value = max(ids_dict.values())
            ids_dict[user] = max_value + 1
        followers = json_object["following"]

        with open('graph.txt', 'a+') as f:
            for user in followers:
                if user not in ids_dict.keys():
                    max_value = max(ids_dict.values())
                    ids_dict[user] = max_value + 1
                f.write(str(ids_dict[id]) + " " + str(ids_dict[user]) + "\n")

parsing_followers()
parsing_following()

