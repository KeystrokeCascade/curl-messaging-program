#!/usr/bin/env python3
'''
cURL Messaging Program

Known issues:
* Cannot exit gracefully on Windows due to ctrl+c not being captured properly in TCP loops
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from socket import socket, timeout, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from signal import signal, SIGINT
from urllib.parse import unquote
from datetime import datetime

# Deal with user input
parser = ArgumentParser(
	description='Simple server that displays messages received with cURL through either HTTP request body, URI query, or raw TCP',
	formatter_class=RawDescriptionHelpFormatter,
	epilog='''To message in Unix:
		$ curl <ip> -d '<message>'
		In Windows:
		> Invoke-WebRequest http://<ip> -Body @{m=\'<message>\'}'''.replace('\t', ''))

parser.add_argument('port', type=int, nargs='?', default=8000, help='port number to bind to')
parser.add_argument('-i', '--ip', action='store_true', help='log message IP address')
parser.add_argument('-t', '--timestamp', action='store_true', help='log message timestamp')
parser.add_argument('-v', '--verbose', action='store_true', help='show full HTTP request')
parser.add_argument('-b', '--buffer', type=int, default=32, help='set TCP buffer size, affects maximum message length')
parser.add_argument('-o', '--timeout', type=float, default=.001, help='set TCP recv timeout until the message is considered completed')
parser.add_argument('-r', '--response', default='', help='HTTP response to serve')
args = parser.parse_args()

# Set up server
serverPort = args.port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
bufferSize = args.buffer
serverSocket.bind(('', serverPort))
serverSocket.listen()

# Set up signal interrupt for graceful exit
def handler(sig, frame):
	serverSocket.close()
	print('Shutting down...')
	exit(0)

signal(SIGINT, handler)

# Serve server continuously
print(f'Server active on port {serverPort}')
while True:
	# Listen and capture message
	connection, address = serverSocket.accept()
	connection.settimeout(args.timeout)
	data = b''
	while True:
		try:
			buffer = connection.recv(bufferSize)
			data += buffer
			if len(buffer) < bufferSize: # Message complete if buffer not full
				break
		except timeout: # Or if the next packet has not been delivered immidiately
			break
	reqMessage = data.decode()

	# Parse HTML headers
	headers = reqMessage.split('\r\n\r\n', 1)
	# Handle raw TCP
	if len(headers) < 2:
		body = headers[0]
		query = ''
	else:
		query = unquote(' '.join(headers[0].split(' ')[1].replace('&', '=').split('=')[1::2])).replace('+', ' ')
		body = headers[-1]

	# Parse and construct logging arguments
	log = ''
	if args.timestamp:
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		log += f'[{timestamp}]'
	if args.timestamp and args.ip:
		log += ' '
	if args.ip:
		log += address[0]
	if log:
		log += ': '

	# Construct message
	message = ''
	if query:
		message += query
	if query and body:
		message += ' '
	if body:
		message += body

	# Log to console
	if args.verbose:
		print(reqMessage)
	else:
		print(f'{log}{message}')

	# Craft minimal 200 HTTP response so no client error
	resMessage = args.response
	resHeader = 'HTTP/1.1 200 OK'
	resContentType = 'Content-Type: text/plain; charset=utf-8'
	resContentLength = f'Content-Length: {len(resMessage)}'

	clientMessage = '\r\n'.join([resHeader, resContentType, resContentLength, '', resMessage])
	connection.sendall(clientMessage.encode())
	connection.close()