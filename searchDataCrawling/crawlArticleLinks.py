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
def main():
	f = open('../snopesDataCrawling/articles_all.json')
	fr = open('../all ratings.txt', 'w')
	calim_rating = json.load(f)
	all_ratings = set()
	number_empty_claim = 0
	for item in calim_rating:
		claim = item['claim']
		if claim == '':
			number_empty_claim += 1
		rating = item['rating']
		claim, x = clean_sentence(claim)
		rating, rating_ = clean_sentence(rating)
		if rating not in all_ratings:
			all_ratings.add(rating)
			if 'FRAUD' in rating:
				print claim
			fr.write(rating+'\n')
			print(rating_)
		#cred = map_rating_cred(rating)
		item['claim'] = claim
		item['rating'] = rating
		#item['cred'] = cred
	print(number_empty_claim)

#search_results = google.search(self.claim, num_page)
main()

