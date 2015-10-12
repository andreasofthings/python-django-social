from unittest import TestCase


class Social(TestCase):
    def setUp(self):
        pass

    def test_tweet(self):
        from social.get import tweets
        result = tweets("http://neumeier.org")
        self.assertEqual(type(()), type(result))
