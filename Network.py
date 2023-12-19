import socket
import threading
import DataManager

def listenUDP(response, user: DataManager.UserInstance):
    threadList = []
    ip = "0.0.0.0" # Listening to all incomming messages
    port = 9999

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((ip, port))

    while True:
        try:
            data, address = udp_socket.recvfrom(1024)
            verify, email = response(data, user)
            if verify:
                udp_socket.sendto(email.encode('utf-8'), address)
                threadList.append(threading.Thread(
                    target=listenTCP,
                    args=(address)
                ))

        except KeyboardInterrupt:
            print('\nStopped.')
            break

    udp_socket.close()

def broadcastUDP(message: str):
    ip = "255.255.255.255"
    port = 9999

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.settimeout(10)
    udp_socket.sendto(message.encode("utf-8"), (ip, port))

    try:
        data, address = udp_socket.recvfrom(1024)
    except TimeoutError:
        raise

    udp_socket.close()

    return (data, address)

def _createTCPSocket(ip, port) -> socket:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((ip, port))

    tcp_socket.listen(10)

    return tcp_socket

def _startClientHandlerThread(csocket):
    thread = threading.Thread(
            target=_handleClient,
            args=(csocket)
    )
    thread.start()

def _handleClient(csocket):
    data = csocket.recv(1024)
    print(f'Received from {csocket}: {data}')

    csocket.send(data)

    csocket.close()

def listenTCP(to: tuple):
    ip, port = to

    tcp_socket : socket = _createTCPSocket(ip, port)

    while True:
        try:
            csocket, address = tcp_socket.accept()
            _startClientHandlerThread(csocket)

        except KeyboardInterrupt:
            print("Stopped")
            break

def sendTCP(to: tuple, data):
    ip, port = to

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((ip, port))
    tcp_socket.send(data.encode('utf-8'))

    data = tcp_socket.recv(1024)
    print(f"Received from server: {data}")

    tcp_socket.close()