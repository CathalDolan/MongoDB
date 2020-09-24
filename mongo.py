import os
import pymongo
if os.path.exists("env.py"):
    import env

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect MongoDB: %s") % e


conn = mongo_connect(MONGO_URI)

coll = conn[DATABASE][COLLECTION]

# new_docs = [{"first": "Mickey", "last": "Pay"},
#    {"first": "sheila", "last": "Murphy"}]
# coll.insert_many(new_docs)


# documents = coll.find()

# for doc in documents:
#    print(doc)
#


# coll.remove({"first": "sheila"})


# coll.update_one({"first": "blue"},
#     {"$set": {"dob": "20/09/1948"}})