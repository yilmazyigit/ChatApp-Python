

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1' # localhost, IP adressi yerel, dyndns
PORT = 23847
BUFFERSIZE = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

def gelen_mesaj():

    while True:
        client,client_address = SERVER.accept()
        print("%s:%s bağlandı." %client_address)
        client.send(bytes("Yılmaz Ayrıcalığıyla Chat Uygulaması!" +
                    "kullanıcı adınızı giriniz: ", "utf8"))
        addresses[client] = client_address
        Thread(target=baglan_client, args=(client,)).start()

def baglan_client(client):

    isim = client.recv(BUFFERSIZE).decode("utf8")
    hosgeldin = "Hosgeldin %s! Çıkmak için {çıkış} yazınız!" %isim
    client.send(bytes(hosgeldin, "utf8"))
    msg = "%s Chat Kanalına Bağlandı!" %isim
    yayin(bytes(msg, "utf8"))
    clients[client] = isim
    while True:
        msg = client.recv(BUFFERSIZE)
        if msg != bytes("{çıkış}", "utf8"):
            yayin(msg, isim+": ")
        else:
            client.send(bytes("{çıkış}","utf8"))
            client.close()
            del clients[client]
            yayin(bytes("%s Kanaldan çıkış yaptı." %isim, "utf8"))
            break

def yayin(msg, prefix=""):

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(10) #maximum 10 bglantıya izin verir!
    print("Bağlantı bekleniyor...")
    ACCEPT_THREAD = Thread(target=gelen_mesaj)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()