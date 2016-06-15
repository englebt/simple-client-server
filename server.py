#!/usr/bin/python

import sys
import socket
import getopt
import threading
import subprocess

def usage():
  print "Simple Server Example"
  print
  print "Usage: server.py [ADDR]:[PORT]"
  print
  print "Examples: "
  print "server.py 127.0.0.1:5000"
  sys.exit(0)

def listen():
  listen_addr = "127.0.0.1"
  listen_port = 5000

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((listen_addr, listen_port))
  server.listen(5)
  print "[*] Listening on %s:%d" % (listen_addr, listen_port)

  while True:
    client_socket, addr = server.accept()

    # Spin off a new thread to handle client
    client_thread = threading.Thread(target=client_handler, 
      args=(client_socket, addr))
    client_thread.start()

def run_command(command):
  # Trim the newline
  command = command.rstrip()

  # Run the command and get the output
  try:
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, 
      shell=True)
  except:
    output = "Failed to execute command.\r\n"

  # Send the output
  return output

def client_handler(client_socket, addr):
  global upload
  global execute
  global command

  while True:
    # Show a prompt
    client_socket.send("<#> ")

    # Receive until we get an EOL
    cmd_buffer = ""

    while "\n" not in cmd_buffer:
      cmd_buffer += client_socket.recv(1024)

    # Send response
    response = run_command(cmd_buffer)
    client_socket.send(response)

def main():
  try:
    # Listen for commands.
    listen()
  except KeyboardInterrupt:
    quit()

main()
