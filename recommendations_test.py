"""Unit tests for recommendations.py"""

__author__ = 'Benedict Chen (benedict@benedictchen.com)'

import recommendations
import unittest



class TestRecommendations(unittest.TestCase):
    """Tests the general functions for recommendations."""

    def test_get_recommendations(self):
        """Tests that get_recommendations finds the correct weighted results."""
        expected_results = [
            (3.3477895267131013, 'The Night Listener'),
            (2.8325499182641614, 'Lady in the Water'),
            (2.5309807037655645, 'Just My Luck')]
        results = recommendations.get_recommendations(recommendations.critics, 'Toby')
        self.assertEqual(results, expected_results)

    def test_transform_preferences(self):
        """Tests the ability to invert the data structure so that movies
        have an associated list of critics instead of the default.
        """
        expected_results = {
            'Lady in the Water': {'Lisa Rose': 2.5, 'Jack Matthews': 3.0, 'Michael Phillips': 2.5,
                                  'Gene Seymour': 3.0, 'Mick LaSalle': 3.0},
            'Snakes on a Plane': {'Jack Matthews': 4.0, 'Mick LaSalle': 4.0, 'Claudia Puig': 3.5,
                                  'Lisa Rose': 3.5, 'Toby': 4.5, 'Gene Seymour': 3.5, 'Michael Phillips': 3.0},
            'Just My Luck': {'Claudia Puig': 3.0, 'Lisa Rose': 3.0, 'Gene Seymour': 1.5, 'Mick LaSalle': 2.0},
            'Superman Returns': {'Jack Matthews': 5.0, 'Mick LaSalle': 3.0, 'Claudia Puig': 4.0, 'Lisa Rose': 3.5,
                                 'Toby': 4.0, 'Gene Seymour': 5.0, 'Michael Phillips': 3.5},
            'The Night Listener': {'Jack Matthews': 3.0, 'Mick LaSalle': 3.0, 'Claudia Puig': 4.5, 'Lisa Rose': 3.0,
                                   'Gene Seymour': 3.0, 'Michael Phillips': 4.0},
            'You, Me and Dupree': {'Jack Matthews': 3.5, 'Mick LaSalle': 2.0, 'Claudia Puig': 2.5, 'Lisa Rose': 2.5,
                                   'Toby': 1.0, 'Gene Seymour': 3.5}
        }
        results = recommendations.transform_preferences(recommendations.critics)
        # Round to 2 places.
        for person in results:
            for movie in results[person]:
                results[person][movie] = round(results[person][movie], 2)
        self.assertDictEqual(results, expected_results)

