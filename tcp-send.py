#!/usr/bin/env python3
'''
TCP Send
'''

from argparse import ArgumentParser
from socket import socket, timeout, AF_INET, SOCK_STREAM

# Deal with user input
parser = ArgumentParser(description='Simple TCP client to send encoded text to a server')
parser.add_argument('host', help='host to send message to')
parser.add_argument('message', help='message to send')
parser.add_argument('-p', '--port', type=int, default=8000, help='port to connect to')
parser.add_argument('-v', '--verbose', action='store_true', help='show TCP response')
parser.add_argument('-b', '--buffer', type=int, default=32, help='set TCP buffer size, affects maximum response length')
parser.add_argument('-t', '--timeout', type=float, default=.5, help='set TCP recv timeout until the message is considered completed')
args = parser.parse_args()

# Set up connection
serverName = args.host
serverPort = args.port
clientSocket = socket(AF_INET, SOCK_STREAM)
bufferSize = args.buffer
message = args.message

# Send message
clientSocket.connect((serverName, serverPort))
clientSocket.sendall(message.encode())

# Handle response
if args.verbose:
	clientSocket.settimeout(args.timeout)
	data = b''
	while True:
		try:
			buffer = clientSocket.recv(bufferSize)
			data += buffer
			if len(buffer) < bufferSize: # Message complete if buffer not full
				break
		except timeout: # Or if the next packet has not been delivered immidiately
			break
	message = data.decode()
	print(message)

clientSocket.close()
