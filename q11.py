from pymongo import MongoClient
import time


def get_name(words):
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
	return new_name


##################################################################
#Read from edges file
##################################################################
client = MongoClient('localhost', 27017)

db = client['mydb']

user_id = input("Enter a disease id:")
start_time = time.time()
user_id1 = 'Disease::' + user_id


with open('edges_test.tsv', 'r') as f:
	next(f)
	treats_disease_id = []
	causes_disease_id= []
	occurs_disease_id = []
	for line in f:
		words = line.split()
##########Treats
		if words[2] == user_id1 and words[1] == "CtD":
			treats_disease_id.append(words[0])
		elif words[0] == user_id1 and words[1] == "DaG":
			causes_disease_id.append(words[2])
		elif words[0] == user_id1 and words[1] == "DlA":
			occurs_disease_id.append(words[2])
f.close
##################################################################
#Creating database Nodes
##################################################################
col = db.create_collection(
name= "disease")

nodes = db[ "disease" ]
with open('nodes_test.tsv', 'r') as f:
	next(f)
	treats_disease_name = []
	causes_disease_name = []
	occurs_disease_name = []
	disease_name = ""
	for line in f:
		words = line.split()
##########Treats
		if words[-1] == "Compound":
			for items in treats_disease_id:
				if items == words[0]:
					treats_disease_name.append(get_name(words))
##########causes
		elif words[-1] == "Gene":
			for items in causes_disease_id:
				if items == words[0]:
					causes_disease_name.append(get_name(words))
		elif words[-1] == "Anatomy":
			for items in occurs_disease_id:
				if items == words[0]:
					occurs_disease_name.append(get_name(words))
		elif words[-1] == "Disease" and words[0] == user_id1:
			disease_name = get_name(words)

result=nodes.insert_one({"d_id": user_id,"disease_name" : disease_name,"treat_disease" : treats_disease_name,"cause_disease" : causes_disease_name,"occurs": occurs_disease_name})
f.close

myquery = { "d_id": user_id}
mydoc = nodes.find(myquery)
for doc in mydoc:
	print(doc)
print("--- %s seconds ---" % (time.time() - start_time))
col.drop()
######################################################################
##################################################################
#Creating database diseases
##################################################################


