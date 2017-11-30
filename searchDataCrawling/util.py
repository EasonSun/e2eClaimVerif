def check_empty(claim, rating, invalidCase):
	if claim == '' and rating == '':
		invalidCase.number_empty_both += 1
	if claim == '':
		invalidCase.number_empty_claim += 1
	if rating == '':
		invalidCase.number_empty_rating += 1

def check_rating(rating, all_ratings, fr):
    if rating not in all_ratings:
        all_ratings.add(rating)
        fr.write(rating + '\n')

def clean_sentence(sen):
	import string
	printable = set(string.printable[:-5])
	cleaned = filter(lambda x: x in printable, sen)
	return cleaned, sen

def map_rating_cred(rating):
    if (('FALSE' in rating and 'MIXTURE' not in rating and 'PHOTOGRAPHS' not in rating)
        or 'MISATTRIBUTED' in rating or 'INCORRECTLY ATTRIBUTED' in rating
        or 'UNPROVEN' in rating):
        return 1
    elif (('TRUE' in rating and 'PARTLY' not in rating and 'OUTDATED' not in rating)
        or ('CORRECTLY ATTRIBUTED' in rating)):
        return 0
