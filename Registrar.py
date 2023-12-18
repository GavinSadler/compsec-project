
import getpass  # Used to make it so inputting passwords shows astericks

import DataManager


def registerUser():
    """User registration routine, will attempt to register a user with the system

    Returns:
        DataManager.UserInstance | None: UserInstance on successful registration, None if there was some error registering the user
    """

    fullName = input("Enter full name: ")
    email = input("Enter email address: ").lower()

    if DataManager.userExists(email):
        print("ERROR: There is already a user registered with that email")
        return None

    password = getpass.getpass("Enter password: ")
    passwordVerify = getpass.getpass("Re-enter password: ")

    print()

    if password != passwordVerify:
        print("ERROR: Passwords did not match, user not registered")
        return None

    print("Passwords match")

    try:
        DataManager.registerUser(email, password)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return

    print("User registered!")

    print()

    user: DataManager.UserInstance

    # Now that the user is registered, try to create a UserInstance for them
    try:
        user = DataManager.UserInstance(email, password)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return

    # Set the fullName field and initialize the contacts field
    user.setUserData({"fullName": fullName, "contacts" : []})

    return user


def loginUser():
    """User login routine, will attempt to login a user with the system

    Returns:
        DataManager.UserInstance | None: UserInstance on successful login, None if there was some error registering the user
    """

    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")

    print()

    user: DataManager.UserInstance

    try:
        user = DataManager.UserInstance(email, password)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return

    return user


def startRoutine() -> DataManager.UserInstance:
    """Routine that runs on the start of the program

    Returns:
        DataManager.UserInstance: The user who shall be logged into the shell
    """

    print()

    print("=================")
    print("   SECURE DROP   ")
    print("=================")

    print()

    # Load in credentials data
    data = DataManager.loadFile()

    # If there are no users registered
    noUsersRegistered = len(data["users"]) == 0
    registerNewUser: bool = False

    if noUsersRegistered: # There are no user registered
        print("No users are registered with this client.")
        registerNewUser = input("Do you want to register a new user (y/n)? ").lower() == "y"

        if registerNewUser: # We create a new user
            user = registerUser()

            if user != None:
                return user

            exit()
        else: # In this case, there are no registered users and the user does not want to register a new user, so we exit
            exit()
    else: # There are user registered
        user = loginUser()

        if user != None:
            return user

        exit()

