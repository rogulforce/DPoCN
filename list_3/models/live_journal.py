import os
import sys
from typing import Optional

import pandas as pd
import requests


class LiveJournal:

    USER_FRIEND_LIST = 'https://www.livejournal.com/misc/fdata.bml?user='
    visited_friends = set()
    network = pd.DataFrame([], columns=['from_node', 'to_node'])

    def get_friends(self, user: str, limit: Optional[int] = None) -> set:
        """ Method getting list of <user> friends from LiveJournal service.

        Result is type(set) because there are some duplicates in the list of friends fetched from the page.

        Args:
            user (str): user name
            limit (Optional[int]): optional limit of obtained friends
        Returns:
            (set) not ordered list of friends.
        """
        url = requests.get(f'{self.USER_FRIEND_LIST}{user}').text.splitlines()[:limit]
        friends = set([it[2:] for it in url[1:-1]])
        return friends

    def explore_network(self, starting_user: str = 'valerois', depth: int = 2,
                        friend_limit: Optional[int] = None) -> None:
        """ Method creating network (dataframe of connections) of friends starting from user <starting_user>
            and obtaining his friends, their friends, friends of their friends... to the given <depth> level.
        Args:
            starting_user (str): Defaults to 'valerois'.
            depth (int): Defaults to 2.
            friend_limit (Optional[int]): optional limit of obtained friends for each of the  users.
        """

        # init values
        current_depth = 1
        self.visited_friends.update([starting_user])

        # take friends of initial user
        friends = [(friend, current_depth) for friend in
                   self.get_friends(user=starting_user, limit=friend_limit)]

        # update visited friends
        self.visited_friends.update(friends)
        friends_queue = friends[:]

        # update network
        rows = pd.DataFrame.from_dict({'from_node': [starting_user] * len(friends), 'to_node': [f[0] for f in friends]})
        self.network = pd.concat([self.network, rows], ignore_index=True)

        while friends_queue:
            # take first node from the queue
            friend, current_depth = friends_queue.pop(0)

            # break condition: current_depth > depth
            if current_depth < depth:
                # get friends
                friends = [(friend_derivative, current_depth+1) for friend_derivative in
                           self.get_friends(user=friend)]

                # extend the network
                rows = pd.DataFrame.from_dict(
                    {'from_node': [friend] * len(friends), 'to_node': [f[0] for f in friends]})
                self.network = pd.concat([self.network, rows], ignore_index=True)

                # working only for depth >= 3, removed for depth == 2 for faster computing
                if depth >= 3:
                    # mark friends to queue as visited
                    friends_to_queue = [friend for friend in friends if friend not in self.visited_friends]
                    self.visited_friends.update(friends_to_queue)

                    # add not yet visited friends to the queue
                    friends_queue.extend(friends_to_queue)

        self.save_network(name=f'{starting_user}_network_depth_{depth}.csv')

    def save_network(self, name: str) -> None:
        """ method saving network to the file
        Args:
            name: name of the file
        """
        self.network.to_csv(name, index=False)


if __name__ == "__main__":
    a = LiveJournal()
    a.explore_network(depth=2)
