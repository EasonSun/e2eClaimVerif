def clean_sentence(sen):
	import string
	printable = set(string.printable[:-5])
	cleaned = filter(lambda x: x in printable, sen)
	if cleaned == '. . FALSE.':
		print sen
	return cleaned, sen
'''
def map_rating_cred(rating):
	if (rating)
'''