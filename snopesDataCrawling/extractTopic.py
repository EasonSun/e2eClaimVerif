import json

filename = 'cleaned_data.json'
topics = set()
outfile = open('topics.txt', 'w')
with open(filename, 'r') as f:
	data = json.load(f)
	for entry in data:
		if entry['topic'] == '':
			topics.add("_")
		else:
			topics.add(entry['topic'])

for topic in topics:
	outfile.write(topics+'\n')