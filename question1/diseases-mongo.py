import csv
from utils import get_collection


nodes = {}
diseases = {}
with open('nodes_test.tsv', 'r') as f:
	tsv_reader = csv.reader(f, delimiter='\t')
	next(tsv_reader)
	for words in tsv_reader:
		node_id, name, kind = words
		if kind == "Disease":
			diseases[node_id] = {
				"node_id": node_id,
				"name": name,
				"compounds_that_treat_disease": set(),
				"compounds_that_palliate_disease": set(),
				"genes": set(),
				"anatomy": set(),
			}
		else:
			nodes[node_id] = {
				"node_id": node_id,
				"name": name,
			}


def is_disease(node_id):
	return node_id in diseases


with open('edges_test.tsv', 'r') as f:
	tsv_reader = csv.reader(f, delimiter='\t')
	next(tsv_reader)
	for words in tsv_reader:
		target = words[2]
		source = words[0]
		metaedge = words[1]
		if is_disease(target):
			disease_id = target
			if metaedge == "CtD":
				diseases[disease_id]['compounds_that_treat_disease'].add(source)
			elif metaedge == "CpD":
				diseases[disease_id]['compounds_that_palliate_disease'].add(source)
		elif is_disease(source):
			disease_id = source
			if metaedge ==  "DaG":
				diseases[disease_id]['genes'].add(target)
			elif metaedge == "DlA":
				diseases[disease_id]['anatomy'].add(target)

coll = get_collection()
for disease_id, disease_data in diseases.items():
	disease_data['compounds_that_palliate_disease'] = [
		nodes[node_id] for node_id in disease_data['compounds_that_palliate_disease']
	]
	disease_data['compounds_that_treat_disease'] = [
		nodes[node_id] for node_id in disease_data['compounds_that_treat_disease']
	]
	disease_data['genes'] = [
		nodes[node_id] for node_id in disease_data['genes']
	]
	disease_data['anatomy'] = [
		nodes[node_id] for node_id in disease_data['anatomy']
	]
	coll.replace_one(
		{"_id": disease_id},
		disease_data,
		upsert=True,
	)

##################################################################
#Read from nodes file
#requires more code because name could consist of many words


#db.inventory.find( { status: "A" }, { item: 1, status: 1, _id: 0 } )
##################################################################
#creating list of ids for disease that user inputs 
##################################################################
##################################################################
#Creating dictionary Nodes
##################################################################
##################################################################
#Creating dictinary Edges
##################################################################
##################################################################

