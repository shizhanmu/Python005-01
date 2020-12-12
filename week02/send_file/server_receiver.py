# 不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端
# 可以传输单个文件的功能。

import socket
import tqdm
from pathlib import Path

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 6001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
UPLOAD_FOLDER = "upload"

def receiver():
    # create the server socket, AF_INET: IPv4,  SOCK_STREAM: TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 1 is the number of max connections allowed
    s.listen(1)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    p1 = Path(filename)
    p2 = Path()
    # set upload folder, create it if it does not exists
    upload = p2 / UPLOAD_FOLDER
    if not upload.exists():
        upload.mkdir()
    p = upload / p1.name
    filename = str(p)
    filesize = int(filesize)

    # instantiates the progress bar object
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)
    # start receving the file from the socket and writing to the file stream
    with open(filename, "ab") as f:
        for _ in progress:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
        progress.close()
        print(f"File '{filename}' has been saved successfully.")
    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()

if __name__ == "__main__":
    receiver()