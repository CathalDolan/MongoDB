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
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a Record")
    print("2. Find a Record by Name")
    print("3. Edit a Record")
    print("4. Delete a Record")
    print("5. Exit")

    option = input("Enter Option: ")
    return option
    

# Helper Function to assist with "Find, Edit & Delete" functions
def get_record():
    print("")
    # Keys used to ID the record are 1st and last
    first = input("Enter Your First Name > ")
    last = input("Enter Your Last Name > ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("Error accessing the database")

    # If there is no record returned, ie nothing in teh cursor object
    if not doc:
        print("")
        print("Doc not found")

    return doc


def add_record():
    print("")
    # Variables to populate dictionary
    first = input("Enter Your First Name > ")
    last = input("Enter Your Last Name > ")
    dob = input("Enter Your DOB > ")
    gender = input("Enter Your Gender > ")
    hair_colour = input("Enter Your Hair Color > ")
    occupation = input("Enter Your Occupation > ")
    nationality = input("Enter Your Nationality > ")
    fav = input("Enter Your Fav > ")

    # Dictionary to insert into teh database
    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_colour": hair_colour,
        "occupation": occupation,
        "nationality": nationality,
        "fav": fav
    }

    # "Try" to insert the dictionary into the database
    try:
        coll.insert(new_doc)
        print("")
        print("Document Inserted")
    except:
        print("Error accessing the database")


def find_record():
    doc = get_record()
    # Check to see if any results are returned
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.lower())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k,v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")

                # If the input is left empty, it doesn't update
                if update_doc[k] == "":
                    update_doc[k] = v

        # Used to confirm that the update was completed
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Doc Updated")
        except:
            print("Error accessing the DB")


def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():

            # Defensive programming approach to give user chance to stop
            if k != "_id":
                print(k.capitalize() + ": " + v.lower())

        print("")
        confirmation = input("Is this the doc you want to delete? \n Y or N > ")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Doc Deleted")
            except:
                print("Error accessing DB")
        else:
            print("Doc not deleted")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            # print("You have selected Option 1")
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid Option")
        print("")

    
conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()
