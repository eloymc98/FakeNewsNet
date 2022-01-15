import json
import os

ids_dict = {}  # dictionary to compress the data

FIRST_ID = 0

# The key is the id, the value is a number from 0 to n-1

def parsing_followers():
    """Parses twitter followers of each user to add these connections to a graph.txt file.
    Each line represents an edge u v.
    """
    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_followers'):  # collect files names
        fileList.append(filenames[2])

    for filenames in fileList:
        for file in filenames:
            filename = 'fakenewsnet_dataset/user_followers/{}'.format(file)
            json_object = json.load(open(filename))

            id = json_object["user_id"]
            if len(ids_dict) == 0:  # if dictionary empty, start it
                ids_dict[id] = FIRST_ID
            if ids_dict.get(id) is None:
                max_value = max(ids_dict.values())  # find max value
                ids_dict[id] = max_value + 1  # value = max + 1
            followers = json_object["followers"]

            with open('graph.txt', 'a+') as f:
                for user in followers:
                    if ids_dict.get(user) is None:
                        max_value = max(ids_dict.values())
                        ids_dict[user] = max_value + 1
                    f.write(str(ids_dict[id]) + " " + str(ids_dict[user]) + "\n")


def parsing_following():
    """Parses twitter following users of each user to add these connections to a graph.txt file.
    Each line represents an edge u v.
    """
    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_following'):
        fileList.append(filenames[2])

    for filenames in fileList:
        for file in filenames:
            filename = 'fakenewsnet_dataset/user_following/{}'.format(file)
            json_object = json.load(open(filename))

            id = json_object["user_id"]
            if len(ids_dict) == 0:
                ids_dict[id] = FIRST_ID
            if ids_dict.get(id) is None:
                max_value = max(ids_dict.values())
                ids_dict[id] = max_value + 1
            followers = json_object["following"]

            with open('graph.txt', 'a+') as f:
                for user in followers:
                    if ids_dict.get(user) is None:
                        max_value = max(ids_dict.values())
                        ids_dict[user] = max_value + 1
                    f.write(str(ids_dict[id]) + " " + str(ids_dict[user]) + "\n")


def parsing_tweets(news_name: str):
    """Parses tweets corresponding to fake news. This is used to select initial infected nodes that start spreading
    fake news."""
    fileList = []
    infected = []

    for filenames in os.walk(f'fakenewsnet_dataset/politifact/fake_subset/{news_name}/tweets'):
        fileList.append(filenames[2])

    for filenames in fileList:
        for file in filenames:
            filename = f'fakenewsnet_dataset/politifact/fake_subset/{news_name}/tweets/{file}'
            json_object = json.load(open(filename))

            id = json_object["user"]["id"]
            if len(ids_dict) == 0:
                ids_dict[id] = FIRST_ID
            if ids_dict.get(id) is None:
                max_value = max(ids_dict.values())
                ids_dict[id] = max_value + 1
            infected.append(ids_dict[id])

            with open('infected.txt', 'w') as f:
                for compressed_id in infected:
                    f.write(str(compressed_id) + "\n")


parsing_followers()
parsing_following()
parsing_tweets(news_name='politifact15014')
