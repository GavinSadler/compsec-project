
import DataManager
import os
import socket

def send(user: DataManager.UserInstance):

    print()
    print("Enter a filename to send: ", end="")
    
    filepath = input()
    
    print()
    
    if not os.path.isfile(filepath):
        print(f"ERROR: '{filepath}' is not a path to a valid file")
        return
    
    filename = os.path.basename(filepath).encode()
    
    print(f"Calculating SHA256 checksum of {filename.decode()}")
    
    fileChecksum = DataManager.getChecksum(filepath)
    
    print("Checksum calculated")
    print()
    print("Enter an IP address and port to attempt to send this file to: ", end="")
    
    host, port = input().split(":")
    
    port = int(port)
    
    if port < 1 or port > 65535:
        print(f"ERROR: port {port} is out of range, enter a port between 1 and 66535")
        return
    
    print()
    print(f"Connecting to {host}:{port} ...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((host, port))
    
    print("Successfully connected to peer")
    print()
    
    with open(filepath, "rb") as fp:
        
        # First, send over the filename
        sock.send(filename)
        
        # Make sure the recipient wants the file
        if sock.recv(1) != b"\x01":
            print("ERROR: Recipient rejected file")
            sock.close()
            return
        
        print(f"Recipient accepted file {filename.decode()}")
        print(f"Sending file checksum: {fileChecksum}")
        
        sock.send(fileChecksum.encode())
        
        # Make sure the recipient has recieved the checksum and that it responds
        if sock.recv(1) != b"\x01":
            print("ERROR: Recipient rejected file")
            sock.close()
            return
        
        # Send the file size to the recipient. This will be used to show progress of sending the file
        sock.send(bytes(os.path.getsize(filepath)))
        
        # Make sure the recipient has recieved the checksum and that it responds
        if sock.recv(1) != b"\x01":
            print("ERROR: Recipient rejected file")
            sock.close()
            return
        
        while True:
            data = fp.read(DataManager.FILE_PARTITION_SIZE)
            
            if not data:
                break
            
            while data:
                sock.send(data)
                data = fp.read(DataManager.FILE_PARTITION_SIZE)

    print(f"Finished sending file {filename.decode()}")
    print()

    sock.close()