import socket

#Name: Ethan Duke
#Pawprint: esdnk7
#Date: 3-18-2023
#Description: server.py, a project implementing socket api to create a chatroom for clients


host = "127.0.0.1"
port = 16656

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()     #set server to listen so clients can connect

clientList = []
usernames = []

def login(message, users):
    username = message.split(" ")[1]
    password = message.split(" ")[2]

    if username in users:
        if password == users[username]:
            return 0    #Successful login
        else:
            return 2    #Password was incorrect
    else:
        return 1    #Username was not found

def newuser(message, users, client):

    #Splits the message up to set username and password variables
    username = message.split(" ")[1]
    password = message.split(" ")[2]

    if username in users:
        client.send("failed".encode('utf-8'))
    else:
        with open("users.txt", "a") as file:
            if file.tell() != 0:
                file.write("\n")    #this will write a new line to users.txt before adding a new user
            file.write(f"({username}, {password})")
        file.close()

        users.update({username: password})      #Adds the newly created user into our users dictionary
        client.send("success".encode('utf-8'))

def logout(usersLoggedIn, client):
    print(usersLoggedIn[0]+" logout")
    temp = usersLoggedIn[0] + " left"  
    del usersLoggedIn[0]    #Since they logged out, it removes that user from this list
    if len(usersLoggedIn) == 0:
        client.send(temp.encode('utf-8'))   #If there are no users in the list, then close the client
        client.close()
    else:
        client.send("failed".encode('utf-8'))

def send(message, usersLoggedIn, client):
    temp = message.split(' ', 1)[1]
    temp = usersLoggedIn[0] + ': ' + temp   #Displays the username, and then appends their message
    print(temp)
    client.send(temp.encode('utf-8'))


#After Main, this function accepts a client, and listens for a message. There are 4 commands that work, and anything else will result in "Unknown Command"
def recieve(users):

    client, address = server.accept()
    print(f"My chat room server. Version One.")

    usersLoggedIn = []  #Keeps track of all of the usernames that are logged in. In V1 of the project we only need to keep track of 1 user/client

    while True:
        message = client.recv(4096).decode('utf-8') #waits for a message from client, and sets variable string to the string that was recieved

        if message.startswith("login"):
            loginResult = login(message, users) #calls login function, and awaits for results to know if there was an error
            if loginResult == 1:
                client.send('Denied: Username Not Found'.encode('utf-8'))
            elif loginResult == 2:
                client.send('Denied: Password is Incorrect'.encode('utf-8'))
            else:
                client.send('Login Confirmed'.encode('utf-8'))
                print(message.split(" ")[1]+" login.")
                usersLoggedIn.append(message.split(" ")[1])
        elif message.startswith("newuser"):
            newuser(message, users, client)
        elif(message.startswith("logout")):
            logout(usersLoggedIn, client)
            client, address = server.accept()
            print(f"Connection Successful")
        elif(message.startswith("send")):
            sendResult = send(message, usersLoggedIn, client)


def Main():
    users = {}

    #Reads file and sets up a dictionary called users, containing all of the usernames and passwords
    file = open('users.txt', 'r')
    for row in file:
        mod = 1
        if(row[len(row)-1] == '\n'):
            mod = 2
        row = row[1:len(row) - mod]
        password = row.split(', ', 2)
        users[password[0]] = password[1]

    file.close()

    recieve(users)  #calls this function to start recieving messages

Main()
