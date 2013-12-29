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



