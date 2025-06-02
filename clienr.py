import socket
import threading
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)

SERVER_IP = '172.16.16.101' 
PORT = 45000

# Fungsi untuk satu client thread
def send_time_request(client_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))

        # Kirim permintaan TIME
        message = "TIME\r\n"
        logging.info(f"[Client-{client_id}] Sending: {repr(message)}")
        sock.sendall(message.encode('utf-8'))

        # Terima respons
        response = sock.recv(1024).decode('utf-8')
        logging.info(f"[Client-{client_id}] Received: {repr(response)}")

        # Tutup dengan QUIT
        quit_message = "QUIT\r\n"
        sock.sendall(quit_message.encode('utf-8'))

    except Exception as e:
        logging.error(f"[Client-{client_id}] Error: {str(e)}")

    finally:
        sock.close()
        logging.info(f"[Client-{client_id}] Connection closed.")

# Jumlah client concurrent yang ingin dijalankan
NUM_CLIENTS = 5

if __name__ == "__main__":
    threads = []

    for i in range(NUM_CLIENTS):
        t = threading.Thread(target=send_time_request, args=(i,))
        threads.append(t)
        t.start()

    # Tunggu semua thread selesai
    for t in threads:
        t.join()

    logging.info("Semua client selesai.")
