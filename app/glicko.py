import math

BASE_RD = 350
BASE_RATING = 1500

def update_RD(periods, old_RD):
	PERIODS_TILL_MAX_UNCERTAINTY = 100
	TYPICAL_RATING_DEVIATION = 50
	# c is a constant, based on the above 2 factors, based on uncertainty in 
	#		player's skill
	c_sq = (BASE_RD**2 - TYPICAL_RATING_DEVIATION**2)/PERIODS_TILL_MAX_UNCERTAINTY
	c = math.sqrt(c_sq)
	
	new_RD = math.sqrt(old_RD**2 + c**2 * periods)
	return math.min(new_RD, 350)

def find_new_rating():
	pass
