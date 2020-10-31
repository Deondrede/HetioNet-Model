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

for i in id:
	words = i.split(":")
	new_word = words[len(words)-2]+":"+words[len(words)-1]
	ids.append(new_word)

##################################################################
#Creating dictionary Nodes
##################################################################

list_counter = 0
total = len(name)
result_nodes= {}
index=1
while list_counter < total:
	result = {"id_source" : id[list_counter],"prof_id" : ids[list_counter],"name" : name[list_counter],"kind":kind[list_counter]}
	result_nodes[index] = result
	list_counter+=1
	index+=1

##################################################################
#Creating dictinary Edges
##################################################################
total = len(sources)
list_counter = 0
result_edges = {}
index = 1
while list_counter < total:
	result = {"prof_id_source" : source[list_counter],"sources" : sources[list_counter],"metaedge" : metaedge[list_counter],"prof_id_target": target[list_counter],"target":targets[list_counter]}
	result_edges[index] = result
	list_counter+=1
	index+=1

disease_name = {}
index=1
for items in result_nodes:
	if result_nodes[items]['kind'] == 'Disease':
		treats = []
		occurs = []
		cause = []
		edges_index = 1
		edges_oindex = 1
		edges_cindex = 1
		result = {"id":result_nodes[items]['prof_id'],"name": result_nodes[items]['name'], "treats": treats,"cause": cause,"occurs":occurs}
		disease_name[index]=result
##################################################################
#treats
##################################################################
		while edges_index <= len(result_edges):
			if result_edges[edges_index]['prof_id_target'] == result_nodes[items]['prof_id'] and result_edges[edges_index]['metaedge'] == 'CtD':
				name = result_edges[edges_index]['prof_id_source']
				for i in result_nodes:
					if result_nodes[i]['prof_id'] == name:
						treats.append(result_nodes[i]['name'])
			edges_index+=1


##################################################################
#occurs
##################################################################

		while edges_oindex <= len(result_edges):
			if result_edges[edges_oindex]['prof_id_source'] == result_nodes[items]['prof_id'] and result_edges[edges_oindex]['metaedge'] == 'DlA':
				name = result_edges[edges_oindex]['prof_id_target']
				for i in result_nodes:
					if result_nodes[i]['prof_id'] == name:
						occurs.append(result_nodes[i]['name'])
			edges_oindex+=1
##################################################################
#cause
##################################################################
		while edges_cindex <= len(result_edges):
			if result_edges[edges_cindex]['prof_id_source'] == result_nodes[items]['prof_id'] and result_edges[edges_cindex]['metaedge'] == 'DaG':
				name = result_edges[edges_cindex]['prof_id_target']
				for i in result_nodes:
					if result_nodes[i]['prof_id'] == name:
						cause.append(result_nodes[i]['name'])
			edges_cindex+=1
		index+=1


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

dict_count = 1
total = len(disease_name)
while dict_count < total+1:
	result=nodes.insert_one({"d_id": disease_name[dict_count]["id"],"disease_name" : disease_name[dict_count]["name"],"treat_disease" : disease_name[dict_count]["treats"],"cause_disease" : disease_name[dict_count]["cause"],"where_disease_occurs" : disease_name[dict_count]["occurs"]})
	dict_count +=1

user_disease_id = input("Enter a Disease id:")
myquery = { "d_id": user_disease_id}
mydoc = nodes.find(myquery)
for doc in mydoc:
	print(doc)

col.drop()

#######################################################################