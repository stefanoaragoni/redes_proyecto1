
# Redes - Proyecto #1 
## XMPP Instant Messaging Client (Python)

This project implements an instant messaging Python client that supports the XMPP (eXtensible Messaging and Presence Protocol) protocol. It supports the following functionalities:

### Account Management

    1. Register a new account on the server
    2. Log in with an account
    3. Log out from an account
    4. Delete the account from the server

### Communication

    1. Display all contacts and their status
    2. Add a user to the contacts
    3. Display contact details of a user
    4. One-on-one communication with any user/contact
    5. Participate in group conversations
    6. Set presence status message
    7. Send/receive notifications
    8. Send/receive files

------

### Downloading the Code

Before you begin, ensure you have the following installed:

    > Python 3.9.2 (64-bit)
    > pip3
    > git

To download the code, open a terminal and run the following commands:

    > cd path/to/your/desired/directory
    > git clone https://github.com/stefanoaragoni/redes_proyecto1.git

Or if you prefer, you can download the code as a ZIP file and extract it to your desired directory.

### Dependencies

To successfully run the XMPP Client, you will need to install several Python libraries. These libraries are essential for various functionalities and communication with the XMPP protocol. You can install them using the following pip3 commands

    > pip3 install slixmpp
    > pip3 install xmpppy
    > pip3 install asyncio
    > pip3 install aioconsole
    > pip3 install prettytable

### Running the Code

In order to run the XMPP Client, you must first run the following command in the terminal:

    > cd path/to/your/desired/directory/redes_proyecto1

Then, run the following command:

    > python3 main.py

------

### Interface

The project is implemented with a console-based interface (CLI). The client is written in Python and is compatible with different operating systems. However, I recommend using Python 3.9.2 (64-bit) since that was the version I used while developing this client. 

### XMPP Server

This XMPP Client automatically uses the domain "alumchat.xyz" for creating new accounts, logging in, adding friends, creating groupchats, etc.. For example:

    > Ingrese su nombre de usuario: test_123

Automatically adds the domain to the username to create the account. 

    > test_123@alumchat.xyz
