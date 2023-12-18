
import base64
import os
import json
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


DATA_FILE_NAME = "userdata.json"


# Create a userdata file if it doesn't already exist
if not os.path.exists(DATA_FILE_NAME):
    with open(DATA_FILE_NAME, "w") as file:
        json.dump({"users": []}, file)


def loadFile():
    """Loads data from DATA_FILE_NAME file and returns it

    Returns:
        Any: object deserialized from json
    """
    data = None

    with open(DATA_FILE_NAME, "r") as fp:
        data = json.load(fp)
        

    return data


def saveFile(data):
    """Saves object passed to data into the DATA_FILE_NAME file

    Args:
        data (Any): json-seriable object that will be written to DATA_FILE_NAME file
    """
    with open(DATA_FILE_NAME, "w") as fp:
        json.dump(data, fp)


def userExists(email: str):
    """Returns whether or not a user is registered with the given email

    Args:
        email (string): the email to check

    Returns:
        Boolean: True if the user exists, False otherwise
    """
    
    data = loadFile()
    
    if [user for user in data["users"] if user["email"] == email.lower()]:
        return True

    return False


def registerUser(email: str, password: str):
    """Registers a user with the system given an email and a password

    Args:
        email (string): the email the user will log in with
        password (string): the password the user will log in with

    Returns:
        Boolean: True if registration was a success, False otherwise
    """
    
    email = email.lower()
    
    # Hash password using bcrypt and then encode it with base64 so we can store it in json
    salt = bcrypt.gensalt()    
    saltB64 = base64.encodebytes(salt).decode()
    hashedPassword = bcrypt.hashpw(bytes(password.encode()), salt)
    hashedPasswordB64 = base64.encodebytes(hashedPassword).decode()

    # Construct the new user object
    newUser = {"email": email, "password": hashedPasswordB64, "salt": saltB64, "data": ""}

    data = loadFile()

    # Make sure the user isn't already registered
    if userExists(email):
        print("ERROR: There is already a user registered with that email")
        return False

    data["users"].append(newUser)

    saveFile(data)

    return True


class UserInstance():
    
    email: str
    encryptor: Fernet
    
    def __init__(self, email: str, password: str):
        """Initializes a UserInstance to operate on encrypted userdata

        Args:
            email (string): the email of the user to verify
            password (string): the password of the user to verify

        Raises:
            RuntimeError: On a email of a user who does not exist
            RuntimeError: On an incorrect password
        """
        
        email = email.lower()
        
        data = loadFile()
        
        # Check to see if the user exists
        if len([user for user in data["users"] if user["email"] == email]) == 0:
            raise RuntimeError("User not found")
        
        user = [user for user in data["users"] if user["email"] == email][0]

        # Load hashed password and salt from file
        hashedPasswordB64: str = user["password"]
        hashedPassword = base64.decodebytes(hashedPasswordB64.encode())
        
        saltB64: str = user["salt"]
        salt = base64.decodebytes(saltB64.encode())
        
        if not bcrypt.checkpw(password.encode(), hashedPassword):
            raise RuntimeError("Incorrect password")
        
        # Generate a key and encryption object to encyrpt/decrypt user data
        kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 10000)
        key = kdf.derive(password.encode())
        keyB64 = base64.urlsafe_b64encode(key)
        
        self.encryptor = Fernet(keyB64)
        self.email = email
    
    
    def getUserData(self):
        
        data = loadFile()
        
        userDataEncrypted: str = [user for user in data["users"] if user["email"] == self.email][0]["data"]
        
        # If user's data field is empty, decryption will fail, so return an empty dict
        if (userDataEncrypted == ""):
            return {}
        
        rawData = self.encryptor.decrypt(userDataEncrypted)
        
        data = json.loads(rawData)
        
        return data

    
    def setUserData(self, userData):
        
        data = loadFile()
        
        userDataSerialized = json.dumps(userData)
        
        userDataEncrypted = self.encryptor.encrypt(userDataSerialized.encode())
        
        [user for user in data["users"] if user["email"] == self.email][0]["data"] = userDataEncrypted.decode()
        
        saveFile(data)