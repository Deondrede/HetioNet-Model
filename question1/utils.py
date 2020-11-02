from pymongo import MongoClient


def get_collection():
	client = MongoClient('localhost', 27017)
	db = client['mydb']
	return db.diseases
