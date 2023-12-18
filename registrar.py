
import os
import json
import getpass # Used to make it so inputting passwords shows astericks
import bcrypt # Used to properly store encrypted passwords
import base64 # Used to encode/decode password hashes

CREDENTIALS_FILE_NAME = "credentials.json"

# Create the default credentials file if it doesn't already exist
if not os.path.exists(CREDENTIALS_FILE_NAME):
    with open(CREDENTIALS_FILE_NAME, "w") as file:
        json.dump({"users": []}, file)

def loadCredentialsData():
    data = None

    try:
        with open(CREDENTIALS_FILE_NAME, "r") as fp:
            data = json.load(fp)
    except Exception as e:
        print(f"ERROR: unable to load credentials file {CREDENTIALS_FILE_NAME}, It may be malformed, or corrupted!")
        exit(1)

    return data


def registerUser():
    fullName = input("Enter full name: ")
    email = input("Enter email address: ").lower()
    password = getpass.getpass("Enter password: ")
    passwordVerify = getpass.getpass("Re-enter password: ")

    print()

    if password != passwordVerify:
        print("Error: Passwords did not match, user not registered!")
        return

    print("Passwords match.")

    # Hash password using bcrypt and then encode it with base64 so we can store it in json
    hashedPassword = bcrypt.hashpw(bytes(password.encode()), bcrypt.gensalt())
    hashedPasswordB64String = base64.encodebytes(hashedPassword).decode()

    # Construct the new user object
    newUser = {"email": email, "password": hashedPasswordB64String, "fullName": fullName}

    # Update credentials json file
    data = loadCredentialsData()

    # Make sure the user isn't already registered
    if [user for user in data["users"] if user["email"] == email]:
        print("There is already a user registered with that email.")
        return

    data["users"].append(newUser)

    with open(CREDENTIALS_FILE_NAME, "w") as fp:
        json.dump(data, fp)

    print("User registered!")
    print()


def verifyUser():
    email = input("Enter email address: ").lower()
    password = getpass.getpass("Enter password: ")

    print()

    data = loadCredentialsData()

    # Check to see if the user exists
    if len([user for user in data["users"] if user["email"] == email]) == 0:
        print(f"Error: user with email '{email}' is not registered with this system")
        return False
    
    user = [user for user in data["users"] if user["email"] == email][0]

    hashedPasswordB64String: str = user["password"]
    hashedPassword = base64.decodebytes(hashedPasswordB64String.encode())

    if user and bcrypt.checkpw(password.encode(), hashedPassword):
        print("Username and password verified, welcome!")
        return True

    print("Error: Unable to verify user, incorrect username or password provided.")
    return False


def loginRoutine():

    # Load in credentials data
    data = loadCredentialsData()

    # If there are no users registered
    noUsersRegistered = (len(data["users"]) == 0)
    if noUsersRegistered:
        print("No users are registered with this client.")

    registerNewUser = (input("Do you want to register a new user (y/n)? ").lower() == "y")
    print()

    if registerNewUser:
        registerUser()
    elif noUsersRegistered:
        exit()
