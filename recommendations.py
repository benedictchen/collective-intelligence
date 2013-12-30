"""
A collection of basic similarity functions from Collective Intelligence.
"""
__author__ = 'Benedict Chen (benedict@benedictchen.com)'

import math

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {
    'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                  'Just My Luck': 3.0, 'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                     'Just My Luck': 1.5, 'Superman Returns': 5.0,
                     'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                         'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                     'The Night Listener': 4.5, 'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                     'Just My Luck': 2.0, 'Superman Returns': 3.0,
                     'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0,
                      'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0}}


def sim_distance(prefs, person1, person2):
    """Calculates the similarity distance between two people, based on
    Euclidian distance.

    Args:
        prefs: A nested dictionary of people and their preferences.
        person1: A string containing the first person to compare.
        person2: A string containing the second person to compare.

    Return:
        A floating point number that represents the distance of similarity
        between the two people.
    """
    shared_items = {}  # The list of shared items.
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1
    # If they have no items in common, then return 0
    if len(shared_items) == 0:
        return 0
    # Add up all the squares of the differences.
    sum_of_squares = sum([
        pow(prefs[person1][item] - prefs[person2][item], 2)
        for item in prefs[person1] if item in prefs[person2]
    ])
    return 1 / (1 + sum_of_squares)


def sim_pearson(prefs, person1, person2):
    """Calculates the similarity between two people using a Pearson
    algorithm, which corrects for 'grade inflation'.  Grade inflation
    is when one person gives higher ratings across the board than the
    other.
    http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient

    Args:
        prefs: A nested dictionary of people and their preferences.
        person1: A string containing the first person to compare.
        person2: A string containing the second person to compare.

    Return:
        A floating point number that represents the distance of similarity
        between the two people.
    """
    # Get the list of mutually rated items.
    shared_items = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1

    # Find the number of elements.
    n = len(shared_items)

    # If nothing in common, return 0
    if n == 0:
        return 0

    # Add up all the preferences.
    sum1 = sum([prefs[person1][item] for item in shared_items])
    sum2 = sum([prefs[person2][item] for item in shared_items])

    # Sum up the squares.
    sum1_sq = sum([pow(prefs[person1][item], 2) for item in shared_items])
    sum2_sq = sum([pow(prefs[person2][item], 2) for item in shared_items])

    # Sum up the products.
    product_sum = sum([prefs[person1][item] * prefs[person2][item]
                      for item in shared_items])

    # Calculate the Pearson score.
    num = product_sum - (sum1 * sum2 / n)
    den = math.sqrt((sum1_sq - pow(sum1, 2) / n) *
                    (sum2_sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den


def get_top_matches(prefs, person, n=5, similarity=sim_pearson):
    """
    Finds the top matches for a given person in similarity.

    Args:
        prefs: A nested dictionary of people and their preferences.
        person: A string containing the first person to compare.
        n: The amount of matches to return.
        similarity: The algorithm used to calculate simiarity.

    Return:
        A list of tuples containing scores and names of matched people..
    """
    scores = [(similarity(prefs, person, person2), person2)
              for person2 in prefs if person2 != person]
    # Sort the result so we have the highest rated showing first.
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    """Gets recommendations for a person using a weighted average
    of every other critic's rankings.

    Args:
        prefs: A nested dictionary of people and their preferences.
        person: A string containing the first person to compare.
        similarity: The algorithm used to calculate simiarity.

    Returns:
        A list of tuples containing scores and item names.
        e.g (0.3, 'Some movie')
    """
    totals = {}
    similarity_sums = {}
    for other_person in prefs:
        # Don't compare me to myself.
        if other_person == person:
            continue
        sim_score = similarity(prefs, person, other_person)
        # Ignore scores of zero or lower.
        if sim_score <= 0:
            continue
        for item in prefs[other_person]:
            # Only score movies I haven't seen yet.
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Rating.
                totals.setdefault(item, 0)
                totals[item] += prefs[other_person][item] * sim_score
                # Sum of similarities.
                similarity_sums.setdefault(item, 0)
                similarity_sums[item] += sim_score
    # Create the normalized list (score, item_name).
    rankings = [(total / similarity_sums[item], item)
                for item, total in totals.items()]
    # Return the sorted list.
    rankings.sort()
    rankings.reverse()
    return rankings


def transform_preferences(prefs):
    """Inverts the preferences so that a given movie has a collection of
    critics and their respective scores for each movie.

    Args:
        prefs: A dictionary of movie critics and scores for each movie.

    Returns:
        An inverted dictionary with movies with critics and scores.
    """
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip the item and person.
            result[item][person] = prefs[person][item]
    return result


def calculate_similar_items(prefs, n=10):
    """
    Finds similar items for each item in a collection.

    Args:
        prefs: A dictionary of movie critics and scores for each movie.

    Returns:
        A dictionary of items with closely related items.
    """
    result = {}
    # Invert the preference matrix to be item centric.
    item_prefs = transform_preferences(prefs)
    count = 10
    for item in item_prefs:
        # Status updates for large datasets.
        count += 1
        if count % 100 == 0:
            print "%d / %d" % (count, len(item_prefs))
        # Find the most similar items to this one.
        scores = get_top_matches(item_prefs, item,
                                 n=n, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(prefs, item_match, user):
    """Finds recommended items ordered by highest rating.

    Args:
        prefs: A dictionary of users/critics and scores for each item.
        item_match: A dictionary of items and their closely related items.
        user: A string containing a given user in the collection(s).

    Returns:
        A list of tuples formatted as (score, item).
    """
    user_ratings = prefs[user]
    scores = {}
    total_similar = {}
    # Loop over the items rated by this user.
    for item, rating in user_ratings.items():
        # Loop over items similar to this one.
        for similarity_score, item2 in item_match[item]:
            # Ignore if user already rated the item.
            if item2 in user_ratings:
                continue
            # Weighted sum of ratings * similarity.
            scores.setdefault(item2, 0)
            scores[item2] += similarity_score * rating
            # Sum of all similarities.
            total_similar.setdefault(item2, 0)
            total_similar[item2] += similarity_score
    # Divide each total score by total weighting to get an average.
    rankings = [(score / total_similar[item], item)
                for item, score in scores.items()]
    # Return the rankings from highest to lowest.
    rankings.sort()
    rankings.reverse()
    return rankings


def load_movie_lens(path="data/movielens"):
    """Loads movie preferences from sample data."""
    # Get movie titles.
    movies = {}
    for line in open(path + '/u.item'):
        uid, title = line.split('|')[0:2]
        movies[uid] = title
    # Load data.
    prefs = {}
    for line in open(path + '/u.data'):
        user, movieid, rating, _ = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs
