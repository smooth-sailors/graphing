from socket import *
import csv
import matplotlib.pyplot as plt
import io

PORT = 54338

def convertToTuples(csv):
    results = [
        tuple(int(x.strip()) for x in line.split(b','))
        for line in csv.split(b'\n')
        if line
    ]

    return results

def graphxy(data):
    print("data: ", data)
    x, y = zip(*data)
    plt.plot(x, y)
    plt.scatter(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('My Graph')
    buf = io.BytesIO()
    plt.savefig(buf, format='pdf')
    plt.clf()
    buf.seek(0)
    pdfBytes = buf.read()
    return pdfBytes

def receive_size(sock, size):
    data = bytearray()
    while len(data) < size:

        recd_data = sock.recv(size - len(data))
        print(len(recd_data))
        if not recd_data:
            break

        data.extend(recd_data)

    return data

def main():
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(("127.0.0.1", PORT))
    serverSock.listen(0)

    while True:
        recSock, addr = serverSock.accept()

        csv_file = 0
        csv_file = bytearray()

        size = int.from_bytes(receive_size(recSock, 8), byteorder='big')
        print(size)

        csv_file = receive_size(recSock, size)

        data = convertToTuples(csv_file)
        print(data)

        pdfBytes = graphxy(data)

        recSock.sendall(len(pdfBytes).to_bytes(8, byteorder='big'))

        recSock.sendall(pdfBytes)

if __name__ == "__main__":
    main()
