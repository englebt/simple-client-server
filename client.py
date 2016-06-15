#!/usr/bin/python

import sys
import socket

def sender(buffer):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  target_host = "127.0.0.1"
  target_port = 5000

  try:
    client.connect((target_host, target_port))

    while True:
      # Wait for response
      recv_len = 1
      response = ""

      while recv_len:
        data = client.recv(4096)
        recv_len = len(data)
        response += data

        if recv_len < 4096:
          break

      print response,

      # Wait for more input
      buffer = raw_input("")
      buffer += "\n"

      # Send buffer
      client.send(buffer)
  except KeyboardInterrupt:
    client.close()
  except:
    print "[*] Exception! Exiting."
    client.close()

def main():
  buffer = ""
  sender(buffer)

main()
