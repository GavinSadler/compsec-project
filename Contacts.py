
import DataManager
import Network

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

    # Use UDP to get the list of users
    userData: dict = user.getUserData()
    contacts = userData["contacts"]

    if len(contacts) == 0:
        print("There are no contacts to list")
        return


    networkInterface = Network
    try:
        print("Looking for active contacts!...")
        contactData, contactIP = networkInterface.broadcastUDP(f"{user.email}")
    except TimeoutError:
        print("Timeout: No user response")
        return

    contactData = contactData.decode('utf-8')
    print(f"{contactData}:{contactIP}")

    for contact in contacts:
        if contact['email'] == contactData:
            user.tempContactList.append((contact, contactIP))
            print(f"{contact['fullName']} <{contact['email']}>")

def verifyContact(email, user: DataManager.UserInstance):
    userData = user.getUserData()
    contacts = userData["contacts"]

    verify = False

    for contact in contacts:
        if email.decode('utf-8') == contact['email']:
            verify = True
            return (verify, user.email)

    return (verify, "")

def send(user: DataManager.UserInstance):
    if len(user.tempContactList) == 0:
        print("No active users, try searching your contacts using 'list'")
        return

    print("Listing online contacts:")

    for index, info in enumerate(user.tempContactList):
        contact, ipInfo = info
        print(f"{index}. {contact['fullName']} <{contact['email']}>")

    contactIndex = input("Select the contact you want to send a message: ")
    contact, ipInfo = user.tempContactList[int(contactIndex)]

    message = input("Message: ")

    networkInterface = Network
    networkInterface.sendTCP(ipInfo, message)