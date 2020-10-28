from pymongo import MongoClient

sources = []
metaedge = []
target = []

with open('sample_edges_1.tsv', 'r') as f:
	next(f)
	for line in f:	
		words = line.split()
		sources.append(words[0])
		metaedge.append(words[1])
		target.append(words[2])	
	print(sources)
	print(metaedge)
	print(target)
f.close

id =[]
name =[]
kind=[]
words_counter=2

with open('sample_nodes_1.tsv', 'r') as f:
	next(f)
	for line in f:
		words = line.split()
		line_len = len(words)
		i = 2
		first_word = 1
		while i < line_len:
			if first_word == 1:
				new_name = words[first_word]
			elif first_word > 1:
				new_name = new_name + ' ' + words[first_word]
			i+=1
			first_word+=1
		name.append(new_name)
		id.append(words[0])
		kind.append(words[-1])
	print(id)
	print(name)
	print(kind)
f.close


client = MongoClient('localhost', 27017)

db = client['mydb']

col = db.create_collection(
name= "nodes")

nodes = db[ "nodes" ]

list_counter = 0
total = len(id)
while list_counter < total:
	result=nodes.insert_one({"name" : name[list_counter],"kind":kind[list_counter]})
	
	list_counter+=1

print("created")
