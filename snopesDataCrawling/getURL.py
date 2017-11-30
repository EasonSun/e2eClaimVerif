import json 

out_file = open('news_url.txt', 'w')
with open('political_news.json') as data_file:
	data = json.load(data_file)
	for data_entry in data:
		out_file.write(data_entry['url']+'\n')
