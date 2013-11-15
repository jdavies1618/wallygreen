import math

"""
Facemash rating system, aka Elo Ratings. See
http://en.wikipedia.org/wiki/Elo_rating_system
for details.
"""
def update_ratings(winning_rating, losing_rating):
	# K is the factor indicating the maximum possible adjustment per game
	# 	We set to 32 for now to keep ratings volatile.
	K = 32 
	winner_expected = get_expected_prob(losing_rating, winning_rating)
	loser_expected = get_expected_prob(winning_rating, losing_rating)
	
	winner_out = winning_rating + K(1 - winner_expected)
	loser_out = losing_rating + K(0 - loser_expected)
	return winner_out, loser_out

def get_expected_prob(score_a, score_b):
	power = (score_b - score_a)/400
	return 1 / (1 + 10**power)
