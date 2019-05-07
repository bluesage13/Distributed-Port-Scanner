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

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
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
        #client_input = receive_input(connection, max_buffer_size)
        client_input = connection.recv(max_buffer_size)
        client_input = client_input.decode("utf8").rstrip()
        # if "--QUIT--" in client_input:
        #     print("Client is requesting to quit")
        #     connection.close()
        #     print("Connection " + ip + ":" + port + " closed")
        #     is_active = False
        # else:
        #     print("Processed result: {}".format(client_input))
        #     connection.sendall("-".encode("utf8"))
        print(client_input)


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    print("Processing the input received from client")

    return "Hello " + str(input_str).upper()

if __name__ == "__main__":
    main()
