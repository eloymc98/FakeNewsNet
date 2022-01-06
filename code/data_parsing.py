import json
import os

ids_dict = {}  # dictionary to compress the data
# The key is the id, the value is a number from 1 to n

def parsing_followers():

    fileList = []

    for filenames in os.walk('fakenewsnet_dataset/user_followers'): # collect files names
        fileList.append(filenames)

    for file in fileList[0][2]: # files stored in 0,2, don't ask me why
        filename = 'fakenewsnet_dataset/user_followers/{}'.format(file)
        json_object = json.load(open(filename))

        id = json_object["user_id"]
        if len(ids_dict) == 0: # if dictionary empty, start it
            ids_dict[id] = 1
        if id not in ids_dict.keys():
            max_value = max(ids_dict.values())  # find max value
            ids_dict[id] = max_value + 1 # value = max + 1
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
            ids_dict[id] = max_value + 1
        followers = json_object["following"]

        with open('graph.txt', 'a+') as f:
            for user in followers:
                if user not in ids_dict.keys():
                    max_value = max(ids_dict.values())
                    ids_dict[user] = max_value + 1
                f.write(str(ids_dict[id]) + " " + str(ids_dict[user]) + "\n")


def parsing_tweets():
    fileList = []
    tweetsList = []
    infected = []

    for filenames in os.walk('fakenewsnet_dataset/politifact/fake_subset'):
        fileList.append(filenames)

    for file in fileList[0][1]:
        for tweetFile in os.walk('fakenewsnet_dataset/politifact/fake_subset/{}/tweets'.format(file)):
            tweetsList.append(tweetFile)

        for tweet in tweetsList[0][2]:
            filename = 'fakenewsnet_dataset/politifact/fake_subset/{}/tweets/{}'.format(file,tweet)
            json_object = json.load(open(filename))

            id = json_object["user"]["id"]
            if len(ids_dict) == 0:
                ids_dict[id] = 1
            if id not in ids_dict.keys():
                max_value = max(ids_dict.values())
                ids_dict[id] = max_value + 1
            infected.append(ids_dict[id])

        with open('infected.txt', 'w') as f:
            for compressed_id in infected:
                    f.write(str(compressed_id) + "\n")


parsing_followers()
parsing_following()
parsing_tweets()

