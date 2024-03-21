# FileShare
A low-level code that uses sockets to communicate between the client and the server. This code uses the python socket library, which maintains the connection between the client and the server.

## about project 
This code is implemented in such a way that the administrator who owns the server package can upload his files with a specific name for each file in the database and up to ten clients can connect to the server.
Each client can download his file with the desired file name .

## structure project

### package server 
This package includes the files `database.py`, `server.py`, `run_server.py`, `handle_client.py`, which is launched with the file `run_server.py` and the file `database.py` is related to be It is the connection to the database and the commands related to the database, and the noteworthy point is that the ``sqlite'' database has been worked on, and another important point is that the initial implementation of the server must be created as a database, which we will deal with in the continuation of the project.

### package client


## diagram-project
![diagram-project](https://raw.githubusercontent.com/AliReza7222/file_share/master/diagram_image/Screen%20Shot%201402-12-26%20at%2012.08.05.png)
