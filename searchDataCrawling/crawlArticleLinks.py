#from google import google
import json
from util import *

'''
given claim, rating
map rating to credibility
with word true : 0 : true
with word false : 1 : false
legend : discard
others : 3 : mix
'''
'''
then search and record article links for each claim
scrape the main text of each article, chop it every 4 sentences
store the snippets in a seperte file named as the idx
'''

class InvalidCase:
	def	__init__(self):
		self.number_empty_claim = 0
		self.number_empty_rating = 0
		self.number_empty_both = 0

all_ratings = set()

def main():
	invalidCase = InvalidCase()
	f = open('../snopesDataCrawling/articles_all.json')
	fr = open('../all ratings.txt', 'w')
	calim_rating = json.load(f)

	for item in calim_rating:
		claim = item['claim']
		rating = item['rating']
		check_empty(claim, rating, invalidCase)
		claim, x = clean_sentence(claim)
		rating, rating_ = clean_sentence(rating)
		check_rating(rating, all_ratings, fr)
		cred = map_rating_cred(rating)
		item['claim'] = claim
		item['rating'] = rating
		item['cred'] = cred


#search_results = google.search(self.claim, num_page)
main()

