from pymongo import MongoClient


##################################################################
#Read from edges file
##################################################################


sources = []
metaedge = []
targets = []

with open('sample_edges_1.tsv', 'r') as f:
	next(f)
	for line in f:	
		words = line.split()
		sources.append(words[0])
		metaedge.append(words[1])
		targets.append(words[2])	
f.close

##################################################################
#Read from nodes file
#requires more code because name could consist of many words
##################################################################

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
f.close

##################################################################
#creating list of ids for disease that user inputs 
##################################################################


target = []
ids = []
source = []
for s in sources:
	words = s.split(":")
	new_word = words[len(words)-2]+":"+words[len(words)-1]
	source.append(new_word)

for t in targets:
	words = t.split(":")
	new_word = words[len(words)-2]+":"+words[len(words)-1]
	target.append(new_word)
print(targets)
print(target)

for i in id:
	words = i.split(":")
	new_word = words[len(words)-2]+":"+words[len(words)-1]
	ids.append(new_word)

##################################################################
#Database section
##################################################################

#open db
client = MongoClient('localhost', 27017)

db = client['mydb']

##################################################################
#Creating database Nodes
##################################################################
col = db.create_collection(
name= "nodes")

nodes = db[ "nodes" ]

list_counter = 0
total = len(name)
while list_counter < total:
	result=nodes.insert_one({"id_source" : id[list_counter],"prof_id" : ids[list_counter],"name" : name[list_counter],"kind":kind[list_counter]})
	
	list_counter+=1

##################################################################
#Creating database Edges
##################################################################
col = db.create_collection(
name= "edges")
total = len(sources)
edges = db[ "edges" ]
list_counter = 0

while list_counter < total:
	result=edges.insert_one({"prof_id_source" : source[list_counter],"sources" : sources[list_counter],"metaedge" : metaedge[list_counter],"prof_id_target": target[list_counter],"target":targets[list_counter]})
	
	list_counter+=1
##################################################################
#Query name from Node collection
##################################################################
disease = input("Enter Disease ID: ")

myquery = { "prof_id": disease}
mydoc = nodes.find(myquery)

for doc in mydoc:
	name = doc["name"]

#data = {"name":,"treatment":,"cause":,"occurs":,}
##################################################################
#Query treatment from Edges collection
##################################################################
myquery = { "prof_id_target": disease,"metaedge" :"CtD"}
mydoc = edges.find(myquery)
treatment_ids = []
for doc in mydoc:
	treatment_ids.append(doc["sources"])


mydoc = []
for items in treatment_ids:
	myquery = { "id_source": items}
	list_of_queries = nodes.find(myquery)
	for l in list_of_queries:
		mydoc.append(l["name"])
print(mydoc)
##################################################################
#Query causes from Edges collection
##################################################################



