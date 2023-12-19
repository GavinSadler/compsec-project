
import Contacts
import DataManager
import Send
import Recieve

def printHelp():
    # TODO: Do help printing with the actual values
    print('\t"add"\t\t-> Add a new contact')
    print('\t"remove"\t-> Removes a contact')
    print('\t"list"\t\t-> List all online contacts')
    print('\t"send"\t\t-> Transfer file on contact')
    print('\t"exit"\t\t-> Exit SecureDrop')

def openShell(user: DataManager.UserInstance):
    while True:
        command = input("secure_drop> ")
        if command == "exit":
            break
        elif command == "help":
            printHelp()
        elif command == "add":
            Contacts.addContact(user)
        elif command == "remove":
            Contacts.removeContact(user)
        elif command == "list":
            Contacts.listContacts(user)
        elif command == "send":
            Send.send(user)
        elif command == "recieve":
            Recieve.recieve(user)
        else:
            print(f"Command '{command}' does not exist: please refer to 'help' for available commands")
