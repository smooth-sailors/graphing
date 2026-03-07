from socket import *
import csv
import matplotlib.pyplot as plot
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

    # convert the data to a usable form
    x, y = zip(*data)

    # plot the data
    plot.plot(x, y)
    plot.scatter(x, y)
    plot.xlabel('x')
    plot.ylabel('y')
    plot.title('Graph')

    # store the bytes of the pdf
    buf = io.BytesIO()
    plot.savefig(buf, format='pdf')
    plot.clf()
    buf.seek(0)

    # return the pddf
    pdfBytes = buf.read()
    return pdfBytes

def receive_size(sock, size):
    data = bytearray()
    # loop until you've received enough data
    while len(data) < size:

        received_data = sock.recv(size - len(data))

        # break if you run out of data to receive
        if not received_data:
            break

        data.extend(received_data)

    return data

def main():
    # open the server socket
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(("127.0.0.1", PORT))
    serverSock.listen(0)

    while True:
        # accept connections
        recSock, addr = serverSock.accept()

        csv_file = bytearray()

        # get the size
        size = int.from_bytes(receive_size(recSock, 8), byteorder='big')

        # recieve the file
        csv_file = receive_size(recSock, size)

        # convert the data to a usable form
        data = convertToTuples(csv_file)

        # graph the data and store it in bytes
        pdfBytes = graphxy(data)

        # send the size of the pdf
        recSock.sendall(len(pdfBytes).to_bytes(8, byteorder='big'))

        # send the pdf
        recSock.sendall(pdfBytes)

if __name__ == "__main__":
    main()
