import socket

#Name: Ethan Duke
#Pawprint: esdnk7
#Date: 3-18-2023
#Description: client.py, a project implementing socket api to create a chatroom for clients

def login(query, client, userLoggedIn):

    client.send(query.encode('utf-8'))
    loginResult = client.recv(4096).decode('utf-8') #Whatever is sent back determines if login was successful or not
    print(loginResult)
    if loginResult == 'Login Confirmed':
        userLoggedIn.append(query.split(" ")[1])    #Add userneame to the list of users logged in
        return True
    else:
        return False

def newuser(query, client):
    username = query.split(" ")[1]
    password = query.split(" ")[2]

    # Some error checking to make sure length requirements are met
    if(len(username) < 3):
        print("Denied: Please make sure username is more than 2 characters long")
    elif(len(username) > 32):
        print("Denied: Please make sure username is less than 33 characters long")
    elif(len(password) < 4):
        print("Denied: Please make sure password is more than 3 characters long")
    elif(len(password) > 8):
        print("Denied: Please make sure password is less than 9 characters long")
    else:
        client.send(query.encode('utf-8'))
        newuserResult = client.recv(4096).decode('utf-8')   #What come back determines if newuser was successful or not
        if newuserResult == 'failed':
            print("Denied: Username already exists")
        else:
            print("New user account created. Please login.")

def send(query, client):
    temp = query.split(' ', 1)[1]
    if(len(temp) > 256):
        print("Denied: Message too long")
    elif(len(temp) < 1):
        print("Denied: Please include a message")
    else:
        client.send(query.encode('utf-8'))
        message = client.recv(4096).decode('utf-8') #This will display the message on the client as well
        print(message)

def logout(query, client):
    client.send(query.encode('utf-8'))
    logoutResult = client.recv(4096).decode('utf-8')    #Indicates the logout message on client as well
    print(logoutResult)

def Main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup socket
    client.connect(('127.0.0.1', 16656))
    print("My chat room client. Version One.")

    loggedIn = False    #This determines if the client is logged in or not
    userLoggedIn = []   #This is a list for the users that are logged in currently
    done = False

    while done == False:
        query = input(">")

        if query.startswith("login"):
            if loggedIn == False:   #if a user is not logged in, then it may proceed
                words = query.split()

                #Error checking to make sure command has right amount of arguments
                if len(words) < 3:
                    print("Denied: Please Include username and password")
                elif len(words) > 3:
                    print("Denied: Too many arguments")
                else:
                    loggedIn = login(query, client, userLoggedIn)   #runs the function and updates loggedIn variable
            else:
                print("Denied: A user is already logged in")
        elif query.startswith("newuser"):
            if loggedIn == False:
                words = query.split()

                #Error checking to make sure command has right amount of arguments
                if len(words) < 3:
                    print("Denied: Please Include username and password")
                elif len(words) > 3:
                    print("Denied: Too many arguments")
                else:
                    newuser(query, client)  #Run newuser function
            else:
                print("Denied: Must log out first")
        elif query.startswith("send"):
            if loggedIn == False:   #Makes sure a user is logged in
                print("Denied: Must be logged in to use this command")
            else:
                words = query.split()

                #Error checking to make sure command has right amount of arguments
                if len(words) < 2:
                    print("Denied: Please follow up with a message to send")
                else:
                    send(query, client)
        elif query.startswith("logout"):
            if loggedIn == False:   #Makes sure a user is logged in
                print("Denied: Must be logged in to use this command")
            else:
                words = query.split()

                #Error checking to make sure command has right amount of arguments
                if len(words) < 1:
                    print("Error")
                elif len(words) > 1:
                    print("Denied: Too many arguments")
                else:
                    logout(query, client)
                    del userLoggedIn[0]
                    loggedIn = False
                    client.close()  #Closes client so that it is officially done, then ends the loop
                    done = True
        else:
            print(">Unknown Command")   #if it isn't one of the 4 commands, it defaults to this message


Main()