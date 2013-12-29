"""
A del.icio.us recommender from Collective Intelligence.
"""
__author__ = 'Benedict Chen (benedict@benedictchen.com)'

import pydelicious


def initialize_user_dict(tag, count=5):
    """Initializes a dictionary of users for later use.
    Args:
        tag: String containing tag to search for in delicious.
        count: Number of results to return.

    Returns:
        A dictionary of users with empty dicts as keys.
    """
    user_dict = {}
    # Get the top count's popular posts.
    for p1 in pydelicious.get_popular(tag=tag)[0:count]:
        # Find all users who posted this.
        for p2 in pydelicious.get_urlposts(p1['url']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict

def fill_items(user_dict):
    all_items = {}
    # Find links posted by all users.
    for user in user_dict:
        for i in range(3):
            try:
                posts = pydelicious.get_userposts(user)
                print posts
                break
            except:
                print "Failed user " + user + ", retrying."
                time.sleep(4)
        for post in posts:
            url = post['url']
            user_dict[user][url] = 1.0
            all_items[url] = 1

        # Fill in the missing items with 0.
        for ratings in user_dict.values():
            for item in all_items:
                if item not in ratings:
                    ratings[item] = 0.0



