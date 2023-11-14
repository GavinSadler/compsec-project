import contacts

def printHelp():
    # TODO: Do help printing with the actual values
    print('\t"add"\t-> Add a new contact')
    print('\t"list"\t-> List all online contacts')
    print('\t"send"\t-> Transfer file on contact')
    print('\t"exit"\t-> Exit SecureDrop')

def executeCommands(command):
    if command == "help":
        printHelp()
    elif command == "add":
        contacts.addContact()
    elif command == "list":
        contacts.listContacts()
    elif command == "send":
        print("--- WIP: please be patient ---")
    else:
        print(f"Command '{command}' does not exist: please refer to 'help' for available commands")

def openShell():
    while True:
        command = input("secure_drop> ")
        if command == "exit":
            break
        else:
            executeCommands(command)
