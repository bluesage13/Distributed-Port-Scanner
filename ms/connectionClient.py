import socket
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8890

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    while True:
        #print("Waiting for input from master")
        input_string = soc.recv(5120)
        print("The number received is ", input_string)
        num = int(input_string)
        sq = num * num
        message = "[" + str(num) + "," + str(sq) + "]"
        soc.sendall(message.encode("utf8"))
        print("Message: ", message)

    soc.close()

if __name__ == "__main__":
    main()
