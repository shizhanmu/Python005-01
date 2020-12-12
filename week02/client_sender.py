import socket
import tqdm
from pathlib import Path

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

def sender():
    # the ip address or hostname of the server, the receiver
    host = "127.0.0.1"
    port = 6001
    # the name of file we want to send
    filename = "Top250.html"
    p = Path(filename)
    # get the file size
    filesize = p.stat().st_size
    # create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # define a progress bar
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)
    # start sending the file
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
        progress.close()
        print(f"File '{filename}' has been transfered successfully.")
    s.close()

if __name__ == "__main__":
    sender()