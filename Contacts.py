
import DataManager

def addContact(user: DataManager.UserInstance):
    """Adds a contact to the given user's contact book
       If the contact already exists, it will not be added

    Args:
        user (DataManager.UserInstance): The user to add a contact to
    """

    fullName = input("Enter Full Name: ")
    email = input("Enter Email Address: ").lower()

    print()

    userData: dict = user.getUserData()

    if len([contact for contact in userData["contacts"] if contact["email"] == email]) != 0:
        print(f"ERROR: A contact with email {email} already exists")
        return

    userData["contacts"].append({"email" : email, "fullName" : fullName})

    user.setUserData(userData)

    print("Contact added!")


def removeContact(user: DataManager.UserInstance):
    """Removes a contact with a provided email

    Args:
        user (DataManager.UserInstance): The user who is removing the contact
    """

    email = input("Enter Email Address: ").lower()

    print()

    userData: dict = user.getUserData()

    matchedContacts = [contact for contact in userData["contacts"] if contact["email"] == email]

    if len(matchedContacts) == 0:
        print(f"No contact with the email {email} was found")
        return

    userData["contacts"][:] = [contact for contact in userData["contacts"] if contact["email"] != email]


def listContacts(user: DataManager.UserInstance):
    """Lists the contacts in a user's contact book

    Args:
        user (DataManager.UserInstance): The user who's contacts will be listed
    """

    userData: dict = user.getUserData()
    contacts = userData["contacts"]

    if len(contacts) == 0:
        print("There are no contacts to list")

    for contact in contacts:
        print(f"{contact['fullName']} <{contact['email']}>")
