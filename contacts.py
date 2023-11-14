import os
import json

CONTACTS_FILE_NAME = "contacts.json"

if not os.path.exists(CONTACTS_FILE_NAME):
    with open(CONTACTS_FILE_NAME, "w") as file:
        json.dump({"contacts": {}}, file)

def loadContactData():
    data = None
    try:
        with open(CONTACTS_FILE_NAME, "r") as fp:
            data = json.load(fp)
    except Exception as e:
        print(f"ERROR: unable to load credentials file {CONTACTS_FILE_NAME}, It may be malformed, or corrupted!")
        exit(1)

    return data

def addContact():
    name = input("Enter Full Name: ")
    email = input("Enter Email Address: ").lower()

    print()

    data = loadContactData()
    data['contacts'][email] = {
        "name": name
    }

    with open(CONTACTS_FILE_NAME, "w") as fp:
        json.dump(data, fp)

    print("Contact added!")

def listContacts():
    data = loadContactData()
    for email in data:
        print(f"{data[email]} <{email}>")
