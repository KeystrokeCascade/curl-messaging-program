# Curl Messaging Program
A server that can intercept plaintext messages in the body of HTTP requests.

CMP can also accept raw TCP data as a message as well, it was made for fun as a bad idea taken to it's illogical extreme.

```
usage: curl-messaging-program.py [-h] [-i] [-t] [-v] [-b BUFFER] [-o TIMEOUT] [-r RESPONSE] [port]

Simple server that displays messages received with cURL through either HTTP request body, URI query, or raw TCP

positional arguments:
  port                  port number to bind to

options:
  -h, --help            show this help message and exit
  -i, --ip              log message IP address
  -t, --timestamp       log message timestamp
  -v, --verbose         show full HTTP request
  -b BUFFER, --buffer BUFFER
                        set TCP buffer size, affects maximum message length
  -o TIMEOUT, --timeout TIMEOUT
                        set TCP recv timeout until the message is considered completed
  -r RESPONSE, --response RESPONSE
                        HTTP response to serve

To message in Unix:
$ curl <ip> -d '<message>'
In Windows:
> Invoke-WebRequest http://<ip> -Body @{m='<message>'}
```

`tcp-send.py` is included as a method to send a message encoded in a raw TCP data stream.

```
usage: tcp-send.py [-h] [-p PORT] [-v] [-b BUFFER] [-t TIMEOUT] host message

Simple TCP client to send encoded text to a server

positional arguments:
  host                  host to send message to
  message               message to send

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to connect to
  -v, --verbose         show TCP response
  -b BUFFER, --buffer BUFFER
                        set TCP buffer size, affects maximum response length
  -t TIMEOUT, --timeout TIMEOUT
                        set TCP recv timeout until the message is considered completed
```