import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Open up a connection
host = socket.gethostname()
port = 8080
s.connect((host,port))

def FileTransfer():                                 #Recieving files

    currentDirectoryBytes = s.recv(4096)            #Recvng files in Server Directory
    currentDirectory = currentDirectoryBytes.decode('utf-8')
    print("Please select a file: \n" + currentDirectory)
    fileName = input(str('Enter File Name: ' ))     #Selecting a file
    fileNameBytes = bytes(fileName,'utf-8')
    if fileName != '':
        s.sendall(fileNameBytes)                    #Sending selection
        dataBytes = s.recv(4096)
        data = dataBytes.decode('utf-8')
        if data[:6] == 'EXISTS':                    #Waiting for user response
            fileSize = data[6:]
            message = input((str('File named "' + fileName + '" is ' + str(fileSize) + ' Bytes. \nDownload(Y/N): ')))
            if message == 'Y' or message == 'y':               #User responds in the affirmative
                print('Starting Download')
                messageBytes = bytes(message,'utf-8')
                s.send(messageBytes)
                with open('new_' + fileName, 'wb') as file:     #Set new name for incoming file
                    data = s.recv(4096)                         #Recvng file
                    totalRecv = len(data)
                    file.write(data)
                    while (totalRecv < int(fileSize)):          #Checking for complete download
                        data = s.recv(4096)
                        totalRecv += len(data)
                        file.write(data)
                        percentDownloaded = '{:0.2f}'.format((totalRecv/float(fileSize))*100)
                        print( str(percentDownloaded)+ '% Downloaded')
                        if totalRecv == int(fileSize):          #Download is complete
                            print('Download Complete. Ending connection with Server. \nGoodbye, Friend-Oh :)')
                            completion = '100'
                            completionBytes = bytes(completion,'utf-8')
                            s.send(completionBytes)
            else:                   #User resonpds in the negative
                print('Cancelling Download. Closing Connection. \nGoodbye, Friend-Oh :)')
                messageBytes = bytes(message,'utf-8')
                s.send(messageBytes)

FileTransfer()

s.close()
