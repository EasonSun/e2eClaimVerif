'''
Clean data crawled from Snopes
'''
import json



def clean(filename):
	output_filename = 'cleaned_data.json'
	stats_filename = 'stats.txt'
	cleaned_data = []

	rating_dict = {
		"true":"true",
		"false":"false",
		"mixture":"mixture",
		"legend":"mixture",
		"mostly true":"mostly true",
		"outdated":"false",
		"undetermined":"mixture",
		"unproven":"mixture",
		"mostly false":"mostly false",
		"mixture of true and false information":"mixture",
		"incorrectly attributed":"false"
	}

	with open(filename) as data_file:    
	    data = json.load(data_file)
	    print len(data)
	    for data_entry in data:
	    	# claim, rating & source must exist
	    	data_entry["rating"] = data_entry["rating"].strip('\n').strip(' ').strip('.').lower()
	    	data_entry["rating"] = remove_nonascii(data_entry["rating"])
	    	if data_entry["claim"].strip() != "" and data_entry["rating"].strip() != "" and data_entry["sources"] != []:
	    		# remove non-ascii characters
	    		data_entry["claim"] = remove_nonascii(data_entry["claim"])
	    		data_entry["content"] = remove_nonascii(data_entry["content"])
	    		data_entry["quotes"] = remove_nonascii(data_entry["quotes"])

	    		# get rid of blank spaces and \n
	    		data_entry["claim"] = data_entry["claim"].strip('\n ')

	    		# clean source info
	    		for s in data_entry["sources"]:
	    			if type(s["publisher"]) is list:
	    				s["publisher"] = ' '.join(s["publisher"])
	    			s["publisher"] = remove_nonascii(s["publisher"])

	    			if type(s["source sentence"]) is list:
	    				s["source sentence"] = ' '.join(s["source sentence"])
	    			s["source sentence"] = remove_nonascii(s["source sentence"])
	    		# remove empty publisher
	    		data_entry["sources"] = [s for s in data_entry["sources"] if s["publisher"] != ""]
	    		if data_entry["sources"] == []:
	    			continue
	    		# remove trailing period of publisher
	    		for s in data_entry["sources"]:
	    			s["publisher"] = s["publisher"].strip(' .')

	    		# clean rating
	    		data_entry["rating"] = data_entry["rating"].strip('\n .:')
	    		# categorize rating into different bins 
	    		if data_entry["rating"] in rating_dict:
	    			data_entry["rating"] = rating_dict[data_entry["rating"]]
	    		else:
	    			continue # give up this entry

	    		data_entry["title"] = remove_nonascii(data_entry["title"])
	    		data_entry["description"] = remove_nonascii(data_entry["description"])
	    		data_entry["category"] = ''.join(data_entry["category"])
	    		data_entry["category"] = remove_nonascii(data_entry["category"])

	    		cleaned_data.append(data_entry)

	with open(output_filename, 'w') as outfile:
		json.dump(cleaned_data, outfile, indent=0)

	# Print stats
	with open(stats_filename, 'w') as outfile:
		outfile.write("Number of data entries: "+str(len(cleaned_data))+'\n')
		ratings = set()
		publishers = set()
		categories_count = {}
		ratings_count = {}
		for d in cleaned_data:
			ratings.add(d["rating"])
			ratings_count[d["rating"]] =  ratings_count.get(d["rating"], 0)+1 # count
			categories_count[d["category"]] = categories_count.get(d["category"], 0)+1
			for s in d["sources"]:
				publishers.add(s["publisher"])
		
		print_separator_line('Ratings', outfile)
		for item in ratings:
  			outfile.write(item+" :  "+ str(ratings_count[item])+"\n" )

  		print_separator_line(' ', outfile)
		outfile.write("\nNumber of ratings: "+str(len(ratings))+'\n')

		print_separator_line('Categories', outfile)
		for item in categories_count:
			outfile.write(item+" :  "+str(categories_count[item])+"\n")
		print_separator_line(' ', outfile)
		outfile.write("\nNumber of categories: "+str(len(categories_count))+'\n')


  		print_separator_line('Publishers', outfile)
		for item in publishers:
  			outfile.write("%s\n" % item)


  		print_separator_line(' ', outfile)
		outfile.write("\nNumber of publishers: "+str(len(publishers))+'\n')

	# extract political news
	political_news = []
	for data_entry in cleaned_data:
		if data_entry["category"] == "Political News":
			political_news.append(data_entry)
	with open("political_news.json", 'w') as outfile:
		json.dump(political_news, outfile, indent=0)
	# print political news
	print_political_news_stats(cleaned_data)
		



def remove_nonascii(str):
	return ''.join([i if ord(i) < 128 else ' ' for i in str])

def print_separator_line(title, f):
	f.write('================================ '+title+' ================================\n')

def print_political_news_stats(cleaned_data):
	political_news = []
	for data_entry in cleaned_data:
		if data_entry["category"] == "Political News":
			political_news.append(data_entry)
	print_stats(political_news, "political_news_stats.txt")


def print_stats(cleaned_data, stats_filename):
	with open(stats_filename, 'w') as outfile:
		outfile.write("Number of data entries: "+str(len(cleaned_data))+'\n')
		ratings = set()
		publishers = set()
		categories_count = {}
		ratings_count = {}
		for d in cleaned_data:
			ratings.add(d["rating"])
			ratings_count[d["rating"]] =  ratings_count.get(d["rating"], 0)+1 # count
			categories_count[d["category"]] = categories_count.get(d["category"], 0)+1
			for s in d["sources"]:
				publishers.add(s["publisher"])
		
		print_separator_line('Ratings', outfile)
		for item in ratings:
  			outfile.write(item+" :  "+ str(ratings_count[item])+"\n" )

  		print_separator_line(' ', outfile)
		outfile.write("\nNumber of ratings: "+str(len(ratings))+'\n')

		print_separator_line('Categories', outfile)
		for item in categories_count:
			outfile.write(item+" :  "+str(categories_count[item])+"\n")
		print_separator_line(' ', outfile)
		outfile.write("\nNumber of categories: "+str(len(categories_count))+'\n')


  		print_separator_line('Publishers', outfile)
		for item in publishers:
  			outfile.write("%s\n" % item)


  		print_separator_line(' ', outfile)
		outfile.write("\nNumber of publishers: "+str(len(publishers))+'\n')

if __name__ == "__main__":
	clean('articles_all.json')