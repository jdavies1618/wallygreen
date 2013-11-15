import unittest2

from app import elo

class TestEloRating(unittest2.TestCase):

	def test_rater(self):
		w, l = elo.update_ratings(1000, 1000)
		self.assertEqual(1016, w)
		self.assertEqual(984, l)

		w, l = elo.update_ratings(600, 1000)
		self.assertGreater(w, 600)
		self.assertLess(l, 1000)

	def test_prob(self):
		p = elo.prob_a_beats_b(1000, 1000)
		self.assertAlmostEqual(1./2, p)

		p = elo.prob_a_beats_b(1000, 600)
		self.assertAlmostEqual(10./11, p)

		p = elo.prob_a_beats_b(1000, 1400)
		self.assertAlmostEqual(1./11, p)
