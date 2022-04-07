import socket
import select
import json
from enum import Enum


class SocketServer(object):
    def __init__(self, encoding=None):
        self._messenger = SocketMessenger(encoding)
        self._messenger.messageDelegate = None

        self.delegate = None

        self.pollFreq = 200
        self.running = False
        self.ip = "0.0.0.0"
        self.port = 8080

    def broadcastMessage(self, message):
        if self.running:
            self._messenger.sendallToMultipleClients(message, self.listOfSockets[1:])
        else:
            self._messenger.delegate_message("!!-Server is not running.")

    def getClientSocket(self):
        for sock in self.listOfSockets[1:]:
            yield sock

    def getClientsIpPort(self):
        for sock in self.listOfSockets[1:]:
            yield self.getClientIpPort(sock)

    # ========================= Polling/Accept/Recieve ================================================#
    def acceptSocket(self, sock):
        # Client is ready to connect
        # socket here is the server socket (sockL)
        (sockClient, addrClient) = sock.accept()
        sockClient.setblocking(False)

        self.listOfSockets.append(sockClient)

        clientID = self.getClientId(sockClient)
        message = "Now connected to WallE"

        # Server socket is always at position 0
        self._messenger.sendallToMultipleClients(message, self.listOfSockets[1:])

        self.delegate.clientConnected(clientID)

    def recieveSocket(self, sock):
        try:
            data = sock.recv(2048)
            if not data:
                self.disconnectClient(sock, True)
            else:
                # A client sent a message
                message = self._messenger.decode(data)
                self._messenger.delegate_message(message)
        except socket.error:
            self._messenger.delegate_message("!!-socket error")
            self.disconnectClient(sock, False)

    def pollMessages(self):
        if self.running:
            tup = select.select(self.listOfSockets, [], [], 0.0)

            # If noone is ready to read from
            if len(tup[0]) == 0:
                return

            sock = tup[0][0]  # First socket ready to read from
            if sock == self.sockL:
                self.acceptSocket(sock)
            else:
                self.recieveSocket(sock)

    # ========================= Connect/Disconnect ================================================#
    def disconnectClientAtIndex(self, index):
        # Adjust index cause Server is always at pos 0
        index += 1
        clientSocket = self.listOfSockets[index]
        self.disconnectClient(clientSocket, True)

    def disconnectClient(self, sock, bMessageClient=None):
        # Adjust index for delegate cause Server is always at pos 0
        # Don't touch server
        index = self.listOfSockets.index(sock) - 1

        if bMessageClient:
            message = "{} (disconnected)".format(self.getClientId(sock))
            defaultMsg = "You have been disconnected from the server."
            self._messenger.sendallToMultipleClients(message, self.listOfSockets[1:], defaultMsg=defaultMsg,
                                                     excluded=[sock])

        sock.close()
        try:
            self.listOfSockets.remove(sock)
        except ValueError:
            return

        self.delegate.clientDisconnectedAtIndex(index)

    def disconnect(self):
        """Take down server"""
        if self.running:
            self._messenger.sendallToMultipleClients("Server closing...", self.listOfSockets[1:])
            # Disconnect all connected clients
            for sock in self.listOfSockets[1:]:
                self.disconnectClient(sock, True)

            self.sockL.close()
            self.sockL = None

        self.running = False

    def connect(self, port=8080):
        """Start up server"""
        try:
            self.port = port
            self.sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sockL.bind((self.ip, self.port))
            self.sockL.listen(5)
            self.sockL.setblocking(False)

            self.listOfSockets = [self.sockL]

            self.running = True
            self._messenger.delegate_message("!!-Server running on: {}".format(self.getIpPort()))
            return True
        except:
            self._messenger.delegate_message("!!-Could not start server")
            return False

    def getClientId(self, clientSocket):
        if clientSocket:
            peername = clientSocket.getpeername()
            return "[{}:{}]".format(peername[0], peername[1])
        else:
            return None

    def getIpPort(self):
        if self.running:
            return "{}:{}".format(self.ip, self.port)

    # ========================= Message Stuff ================================================#


class Encoding(Enum):
    utf8 = "utf-8"
    ascii = "ascii"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SocketMessenger():
    def __init__(self, encoding):
        if Encoding.has_value(encoding):
            self.encoding = encoding.value
        else:
            self.encoding = Encoding.utf8.value

        self.messageDelegate = None

    def sendallToMultipleClients(self, message, clients, *, defaultMsg=None, excluded=[]):
        """Send message to multiple clients

        For single threaded use.
        Default message sends to everyone in Excluded
        """
        try:
            for client in clients:
                if client not in excluded:
                    client.sendall(self.encode(message))
                elif defaultMsg is not None:
                    client.sendall(self.encode(defaultMsg))
        except ConnectionAbortedError:
            pass
        return True

    def delegate_message(self, message):
        try:
            if self.messageDelegate is not None:
                self.messageDelegate.message(message)
        except:
            pass

    def encode(self, msg):
        return bytearray(msg, self.encoding)

    def decode(self, bArr):
        return bArr.decode(self.encoding)

