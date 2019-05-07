import socket
import sys
import traceback
from threading import Thread


def main():
    startUser()


def startUser():
    host = "127.0.0.1"
    port = 8889

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        soc.bind((host, port))
    except Exception as e:
        print(e)
        sys.exit()

    soc.listen(5)
    print("Socket now listening")
    
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        message = input("Enter Data: ")
        connection.sendall(message.encode("utf8"))
        client_input = connection.recv(max_buffer_size)
        client_input = client_input.decode("utf8").rstrip()
        print(client_input)

if __name__ == "__main__":
    main()
