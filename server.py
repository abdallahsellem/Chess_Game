from socket import * 

from threading import * 


# Connection Data
host = '127.0.0.1'
port = 7000


def receive(receiverClient,senderClient):
    
    while True :
        message=senderClient.recv(1024)
        receiverClient.send(message)
        
    


def main():

    server=socket(AF_INET,SOCK_STREAM) 
    server.bind((host,port))
    server.listen()
    try:
        #configure and send Configuration to the first one connecting me 
        client1,address1=server.accept() 
        client2,address2=server.accept() 
        
        client1.send("1".encode("utf-8")) 
        client2.send("2".encode("utf-8")) 
        
        thread1=Thread(target=receive,args=(client1,client2))
        thread2=Thread(target=receive,args=(client2,client1))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except Exception as ex :
        print(ex)
        client1.close()
        client2.close()
        server.close()


if __name__ == "__main__":
    main()
