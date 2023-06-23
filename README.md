# ChatRoom
A project implementing socket api to create a chatroom for clients

# Instructions:
* Make sure Python3 is installed
* Run server.py by typing the command ```python3 server.py```
* Once that is running, run a client by typing ```python3 client.py```

# Application Manual
* There are 4 different commands this application offers: login, newuser, send, and logout
* The Login function must be laid out as such: ```login username password```
  * This function can only be used if the current client is not already logged in
  * Valid usernames and passwords are stored in the users.txt file
* The Newuser function must be laid out as such: ```newuser username password```
  * This function will error check and make sure the user being created doesn't already exist
  * This function can only be used if the client is not already logged in
* The Send function must be laid out as such: ```send message```
  * The send function can only be used if the client is logged in
* The Logout function must be laid out as such: ```logout```
  *This function can only be used if the client is not already logged in
