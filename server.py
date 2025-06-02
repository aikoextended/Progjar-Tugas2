from socket import *
import socket
import threading
import logging
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO)

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                data = self.connection.recv(1024)  # buffer besar untuk menangkap semua
                if not data:
                    break

                request = data.decode('utf-8')
                logging.info(f"Received request from {self.address}: {repr(request)}")

                # Mengecek jika request adalah "TIME\r\n"
                if request.strip() == "TIME":
                    now = datetime.now()
                    jam = now.strftime("%H:%M:%S")
                    response = f"JAM {jam}\r\n"
                    self.connection.sendall(response.encode('utf-8'))

                # Mengecek jika request adalah "QUIT\r\n"
                elif request.strip() == "QUIT":
                    logging.info(f"Connection with {self.address} closed by client request.")
                    break

                else:
                    logging.warning("Invalid request received")
        except Exception as e:
            logging.error(f"Error handling client {self.address}: {str(e)}")
        finally:
            self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.info("Time server listening on port 45000")

        while True:
            connection, client_address = self.my_socket.accept()
            logging.info(f"Connection from {client_address}")
            client_thread = ProcessTheClient(connection, client_address)
            client_thread.start()
            self.the_clients.append(client_thread)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
