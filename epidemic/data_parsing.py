import json
import os


class DataParser(object):

    def __init__(self, include_user_following: bool, news: dict):
        self.include_user_following = include_user_following
        self.FIRST_USER_ID = 0
        self.news = news

    def generate_network(self, news: list, news_type: str):
        """Builds a network from tweets and user connections on Twitter"""
        user_ids_dict = dict()  # dictionary to map the user_ids. The key is the id, the value is a number from 0 to n-1
        infected = set()
        infected_raw = list()

        if news_type == 'fake':
            network = 'FNN'
        else:
            network = 'TNN'

        graph = open(f'graph_data/graph_{network}.txt', 'w')
        edges = set()

        print(f"Starting {network} graph generation...\n")

        for news_name in news:
            print(f"Parsing {news_name} tweets...\n")

            file_list = list()
            for filenames in os.walk(f'fakenewsnet_dataset/politifact/{news_type}_subset/{news_name}/tweets'):
                file_list.append(filenames[2])

            # Get initial nodes that spread the news (infected nodes)
            for filenames in file_list:
                for file in filenames:
                    if file.endswith(' 2.json'):  # Skip duplicated tweets
                        continue
                    filename = f'fakenewsnet_dataset/politifact/{news_type}_subset/{news_name}/tweets/{file}'
                    json_object = json.load(open(filename))

                    user_id = json_object["user"]["id"]

                    # Compress user id
                    if len(user_ids_dict) == 0:
                        user_ids_dict[user_id] = self.FIRST_USER_ID
                    if user_ids_dict.get(user_id) is None:
                        max_value = max(user_ids_dict.values())
                        user_ids_dict[user_id] = max_value + 1

                    # Indicate user as infected
                    if user_ids_dict[user_id] not in infected:
                        infected.add(user_ids_dict[user_id])
                        infected_raw.append(user_id)

            print(f"Parsing {news_name} related users' followers...\n")
            # Once we have the initially infected nodes, build edgelist of connections in social media
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

            if self.include_user_following:
                print(f"Parsing {news_name} related users' followees...\n")
                # Add user following connections
                for infected_node in infected_raw:
                    try:
                        filename = f'fakenewsnet_dataset/user_following/{infected_node}.json'
                        infected_id = user_ids_dict[infected_node]
                        json_object = json.load(open(filename))
                        for follower_id in json_object['following']:
                            if user_ids_dict.get(follower_id) is None:
                                max_value = max(user_ids_dict.values())
                                user_ids_dict[follower_id] = max_value + 1
                            user_id = user_ids_dict[follower_id]
                            if (infected_id, user_id) not in edges and (user_id, infected_id) not in edges:
                                graph.write(f'{infected_id} {user_id}\n')
                    except Exception as e:
                        print(e)

        # Write infected nodes
        with open(f'graph_data/infected_{network}.txt', 'w') as f:
            for compressed_id in infected:
                f.write(str(compressed_id) + "\n")

        # Write max id to file
        with open(f'graph_data/params_{network}.txt', 'w') as f:
            max_value = str(max(user_ids_dict.values(), default=0) + 1)
            f.write(max_value)

        print(f"{network} graph generated!\n")
        graph.close()

    def generate_spreaders_network(self, news: list, news_type: str):
        """Builds a network from tweets and user connections on Twitter"""
        user_ids_dict = dict()  # dictionary to map the user_ids. The key is the id, the value is a number from 0 to n-1
        infected = set()
        infected_raw = list()

        if news_type == 'fake':
            network = 'FNN'
        else:
            network = 'TNN'

        graph = open(f'graph_data/graph_{network}.txt', 'w')
        edges = set()

        print(f"Starting {network} graph generation...\n")

        for news_name in news:
            print(f"Parsing {news_name} tweets...\n")

            file_list = list()
            for filenames in os.walk(f'fakenewsnet_dataset/politifact/{news_type}_subset/{news_name}/tweets'):
                file_list.append(filenames[2])

            # Get initial nodes that spread the news (infected nodes)
            for filenames in file_list:
                for file in filenames:
                    if file.endswith(' 2.json'):  # Skip duplicated tweets
                        continue
                    filename = f'fakenewsnet_dataset/politifact/{news_type}_subset/{news_name}/tweets/{file}'
                    json_object = json.load(open(filename))

                    user_id = json_object["user"]["id"]

                    # Compress user id
                    if len(user_ids_dict) == 0:
                        user_ids_dict[user_id] = self.FIRST_USER_ID
                    if user_ids_dict.get(user_id) is None:
                        max_value = max(user_ids_dict.values())
                        user_ids_dict[user_id] = max_value + 1

                    # Indicate user as infected
                    if user_ids_dict[user_id] not in infected:
                        infected.add(user_ids_dict[user_id])
                        infected_raw.append(user_id)

        print(f"Parsing users' followers...\n")
        # Once we have the initially infected nodes, build edgelist of connections in social media
        for infected_node in infected_raw:
            try:
                filename = f'fakenewsnet_dataset/user_followers/{infected_node}.json'
                infected_id = user_ids_dict[infected_node]
                json_object = json.load(open(filename))
                for follower_id in json_object['followers']:
                    if user_ids_dict.get(follower_id) is not None: # If user is infected, include it in the graph
                        user_id = user_ids_dict[follower_id]
                        if (infected_id, user_id) not in edges and (user_id, infected_id) not in edges:
                            graph.write(f'{infected_id} {user_id}\n')
            except Exception as e:
                print(e)

        if self.include_user_following:
            print(f"Parsing related users' followees...\n")
            # Add user following connections
            for infected_node in infected_raw:
                try:
                    filename = f'fakenewsnet_dataset/user_following/{infected_node}.json'
                    infected_id = user_ids_dict[infected_node]
                    json_object = json.load(open(filename))
                    for follower_id in json_object['following']:
                        if user_ids_dict.get(follower_id) is not None: # If user is infected, include it in the graph
                            user_id = user_ids_dict[follower_id]
                            if (infected_id, user_id) not in edges and (user_id, infected_id) not in edges:
                                graph.write(f'{infected_id} {user_id}\n')
                except Exception as e:
                    print(e)

        # Write infected nodes
        with open(f'graph_data/infected_{network}.txt', 'w') as f:
            for compressed_id in infected:
                f.write(str(compressed_id) + "\n")

        # Write max id to file
        with open(f'graph_data/params_{network}.txt', 'w') as f:
            max_value = str(max(user_ids_dict.values(), default=0) + 1)
            f.write(max_value)

        print(f"{network} graph generated!\n")
        graph.close()

    def generate_fnn_and_tnn_networks(self):
        """Parses tweets corresponding to all available news. Build a graph corresponding to fake news and another graph
        corresponding to true news."""
        self.generate_network(news=self.news['fake'], news_type='fake')
        self.generate_network(news=self.news['true'], news_type='real')

    def generate_fnn_and_tnn_spreaders_networks(self):
        """Parses tweets corresponding to all available news. Build a graph corresponding to fake news and another graph
        corresponding to true news."""
        self.generate_spreaders_network(news=self.news['fake'], news_type='fake')
        self.generate_spreaders_network(news=self.news['true'], news_type='real')


if __name__ == '__main__':
    news = {'true': ['politifact13136', 'politifact14064'], 'fake': ['politifact15178', 'politifact15371']}
    parser = DataParser(include_user_following=True, news=news)
    parser.generate_fnn_and_tnn_spreaders_networks()
