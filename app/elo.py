import math

"""
Facemash rating system, aka Elo Ratings. See
http://en.wikipedia.org/wiki/Elo_rating_system
for details.
"""

DEFAULT_RATING = 1600.0


def update_ratings(winning_rating, losing_rating):
	# K is the factor indicating the maximum possible adjustment per game
	# 	We set to 32 for now to keep ratings volatile.
	K = 32.0
	winner_expected = prob_a_beats_b(winning_rating, losing_rating)
	loser_expected = prob_a_beats_b(losing_rating, winning_rating)

	winner_upd = K*(1 - winner_expected)
	loser_upd = K*(0 - loser_expected)
	winner_out = winning_rating + winner_upd
	loser_out = losing_rating + loser_upd
	return winner_out, loser_out

def prob_a_beats_b(score_a, score_b):
	power = (score_b - score_a)/400
	return 1.0 / (1 + 10**power)
