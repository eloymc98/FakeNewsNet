import json
import os

ids_dict = {} #dictionary to compress the data

def parsing_followers():

    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_followers'):
        fileList.append(filenames)

    for file in fileList[0][2]:
        filename = 'fakenewsnet_dataset/user_followers/{}'.format(file)
        json_object = json.load(open(filename))

        id = json_object["user_id"]
        followers = json_object["followers"]

        with open('graph.txt', 'a+') as f:
            for user in followers:
                f.write(str(id) + " " + str(user) + "\n")


def parsing_following():

    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_following'):
        fileList.append(filenames)

    for file in fileList[0][2]:
        filename = 'fakenewsnet_dataset/user_following/{}'.format(file)
        json_object = json.load(open(filename))

        id = json_object["user_id"]
        followers = json_object["following"]

        with open('graph.txt', 'a+') as f:
            for user in followers:
                f.write(str(id) + " " + str(user) + "\n")

parsing_followers()
parsing_following()

