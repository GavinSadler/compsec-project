
import DataManager
import os
import socket

LISTEN_TIMEOUT = 1
RECIEVED_FILES_DIR = "./RecievedFiles"

# Create the directory to recieve files from if it doesn't already exist
if not os.path.exists(RECIEVED_FILES_DIR):
    os.mkdir(RECIEVED_FILES_DIR)

def recieve(user: DataManager.UserInstance):
    
    print()
    print("Enter a port to recieve from: ", end="")
    
    port = int(input())
    
    if port < 1 or port > 65535:
        print(f"ERROR: port {port} is out of range, enter a port between 1 and 66535")
        return
    
    host = socket.gethostbyname(socket.gethostname())
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    sock.settimeout(LISTEN_TIMEOUT * 60)
    
    print(f"Listening on {host}:{port} for {LISTEN_TIMEOUT} minute(s)")
    print()
    
    peer, address = sock.accept()
    
    print(f"Accepting connection from {address[0]}:{address[1]}")
    print()
    
    filename = peer.recv(1024).decode()
    
    print(f"File to recieve: {filename}")
    
    # Send 0x01 as a confirmation
    peer.send(b"\x01")
    
    fileChecksum = peer.recv(1024).decode()
    
    print(f"File SHA256 checksum: {fileChecksum}")
    print()
    
    # Send 0x01 as a confirmation
    peer.send(b"\x01")
    
    with open(RECIEVED_FILES_DIR + "/" + filename, "wb") as fp:
        
        data = peer.recv(DataManager.FILE_PARTITION_SIZE)
        
        while data:
            
            fp.write(data)
            data = peer.recv(DataManager.FILE_PARTITION_SIZE)
            
    
    print(f"File successfully recieved")
    print()
    
    print(f"Verifying checksum")
    
    recievedChecksum = DataManager.getChecksum(RECIEVED_FILES_DIR + "/" + filename)
    
    if recievedChecksum == fileChecksum:
        print("Checksums match")
    else:
        print()
        print(f"ERROR: Checksum does not match what was sent")
        print()
        print(f"Sent checksum:\t{fileChecksum}")
        print(f"Recieved checksum:\t{recievedChecksum}")

    sock.close()