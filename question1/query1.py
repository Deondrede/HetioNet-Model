from utils import get_collection
import time

coll = get_collection()


disease_id = input("Input an ID:")
disease_id = "Disease::" + disease_id
myquery = {"_id":disease_id}
start_time = time.time()
mydoc = coll.find(myquery)
print("--- %s seconds ---" % (time.time() - start_time))
for doc in mydoc:
	print(doc)