import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Open up a connection
host = socket.gethostname()
port = 8080
s.bind((host,port))

s.listen(5)
print('Waiting for incoming connections')


client, address = s.accept()                    #Accept incoming connection request, creat 'client' instance
print('Connected to ' + host + str(address))

def FileTransfer():                                 #Sending files

    selectFile = str(os.listdir())                  #List Directory Items in which Server is present
    selectFileBytes = bytes(selectFile,'utf-8')     #Convert information to bytes
    client.send(selectFileBytes)                    #Send information to Client
    fileNameBytes = client.recv(4096)               #Recieve wanted file name from client, 4096 bytes recvd at a time
    fileName = fileNameBytes.decode('utf-8')
    print("This file has been selected: " + fileName + "\nWaiting for Client Response")
    if os.path.isfile(fileName):                    #Collecting and sending information in for selected file
        information = bytes('EXISTS' + str(os.path.getsize(fileName)),'utf-8')
        fileSize = os.path.getsize(fileName)
        client.sendall(information)
        clientResponseBytes = client.recv(4096)
        clientResponse = clientResponseBytes.decode('utf-8')
        if clientResponse == 'Y' or clientResponse == 'y':            #Send file if client responds affirmative
            print('The Client chose YES. Commencing Upload')
            file = open(fileName,'rb')              #Opening selected file, converting to bytes
            data = file.read(4096)
            totalSent = len(data)
            client.sendall(data)
            while (totalSent < fileSize):           #Checking how much data is sent
                data = file.read(4096)
                totalSent += len(data)
                client.sendall(data)
                percentUploaded = '{:0.2f}'.format((totalSent/float(fileSize))*100)
                print(str(percentUploaded)+ '% Uploaded')
                if totalSent == fileSize:           #Message at completion
                    completionBytes = client.recv(4096)
                    completion = completionBytes.decode('utf-8')
                    if completion == '100':
                        print('Upload complete. Ending connection with Client. \nGoodbye :)')
        else:                                       #Client responds in the negative
            print('Will not be downloading anything. Closing Connection. \nThank you, Friend-Oh :)')

FileTransfer()

s.close()
