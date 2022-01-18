import json
import os

FIRST_ID = 0

def process_news(news_name: str, type: str):
    """Parses tweets corresponding to the indicated news. This is used to select initial infected nodes that start
    spreading the news, and to build a network of the people that can be reached from these initial spreaders."""

    user_ids_dict = dict()  # dictionary to map the user_ids. The key is the id, the value is a number from 0 to n-1
    file_list = list()
    infected = set()
    infected_raw = list()

    for filenames in os.walk(f'fakenewsnet_dataset/politifact/{type}_subset/{news_name}/tweets'):
        file_list.append(filenames[2])

    # Get initial nodes that spread the news (infected nodes)
    for filenames in file_list:
        for file in filenames:
            filename = f'fakenewsnet_dataset/politifact/{type}_subset/{news_name}/tweets/{file}'
            json_object = json.load(open(filename))

            user_id = json_object["user"]["id"]

            # Compress user id
            if len(user_ids_dict) == 0:
                user_ids_dict[user_id] = FIRST_ID
            if user_ids_dict.get(user_id) is None:
                max_value = max(user_ids_dict.values())
                user_ids_dict[user_id] = max_value + 1

            # Indicate user as infected
            if user_ids_dict[user_id] not in infected:
                infected.add(user_ids_dict[user_id])
                infected_raw.append(user_id)

    # Once we have the initially infected nodes, build edgelist of connections in social media
    graph = open(f'graph_{news_name}_{type}.txt', 'w')
    edges = set()
    for infected_node in infected_raw:
        try:
            filename = f'fakenewsnet_dataset/user_followers/{infected_node}.json'
            infected_id = user_ids_dict[infected_node]
            json_object = json.load(open(filename))
            for follower_id in json_object['followers']:
                if user_ids_dict.get(follower_id) is None:
                    max_value = max(user_ids_dict.values())
                    user_ids_dict[follower_id] = max_value + 1
                user_id = user_ids_dict[follower_id]
                if (infected_id, user_id) not in edges and (user_id, infected_id) not in edges:
                    graph.write(f'{infected_id} {user_id}\n')
        except Exception as e:
            print(e)

    graph.close()

    # Write infected nodes
    with open(f'infected_{news_name}_{type}.txt', 'w') as f:
        for compressed_id in infected:
            f.write(str(compressed_id) + "\n")

    # Write max id to file
    with open(f'params_{news_name}_{type}.txt', 'w') as f:
        max_value = str(max(user_ids_dict.values(), default=0) + 1)
        f.write(max_value)


if __name__ == '__main__':
    news = [('politifact15014', 'fake'), ('politifact1084', 'real')]
    for (name, type) in news:
        process_news(news_name=name, type=type)
