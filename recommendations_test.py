"""Unit tests for recommendations.py"""

__author__ = 'Benedict Chen (benedict@benedictchen.com)'

import recommendations
import unittest



class TestRecommendations(unittest.TestCase):
    """Tests the general functions for recommendations."""

    def test_get_recommendations(self):
        expected_results = [
            (3.3477895267131013, 'The Night Listener'),
            (2.8325499182641614, 'Lady in the Water'),
            (2.5309807037655645, 'Just My Luck')]
        results = recommendations.get_recommendations(recommendations.critics, 'Toby')
        self.assertEqual(results, expected_results)

