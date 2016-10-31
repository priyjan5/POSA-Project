"""
   file: launch.py
   vers: 1.4
   desc: Openstack Tor Network builder backend
"""

import time
import getpass
from novaclient.client import Client


# Logging functions

def logger(access,session,debug,error):
    """
       TODO: implement
    """
    if access is not None:
        # Log to access log
    if session is not None:
        # Log to session log
    if debug is not None:
        # Log to debug log
    if error is not None:
        # Log to error log

# Connection functions

def get_auth(username,password):
    """
       TODO: remove hardcoded variables

       Dictionary for user authentication parameters

       Function of:
           create_connection

       Args:
           username - RIT DCE username
           password - RIT DCE password

       Returns:
           auth - dictionary for authenticating to openstack keyauth
    """
    username = username + "@ad.rit.edu"
    auth = {}
    auth['version'] = '2'
    auth['insecure'] = True
    auth['username'] = username
    auth['password'] = password
    auth['auth_url'] = 'https://acopenstack.rit.edu:5000/v2.0'
    auth['project_id'] = 'jrh7130-multi'
    if auth['insecure'] = True:
        cert_warn = "Connection: SSL certificates being ignored"
        logger(cert_warn,None,cert_warn,None)
    return auth

def create_connection(username,password):
    """
        Creates a nova client with given authentication parameters

        Function of:
           main
           web_launch
           
        Args:
           none

        Returns:
           nova_client - object to query openstack
    """
    if username is None:
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        logger("Client initialized by " + username + " from command line",None,None,None)
    auth = get_auth()
    nova_client = Client(**auth)
    return nova_client

# List functions

def list_hub(client):
    """
       Menu for reporting related functions

       Function of:
          main
    """
    while(True):
        print("\nBackend Reporting Functions")
        print("1. List Instances")
        print("2. List Images")
        print("3. List Flavors")
        print("4. List Networks")
        print("5. Return to Main Menu")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            list_instances(client)
        elif case == 2:
            list_images(client)
        elif case == 3:
            list_flavors(client)
        elif case ==4:
            list_networks(client)
        elif case == 5:
            return
        else:
            print("\nInvalid option")

def list_instances(client):
    """
       Lists available instances

       Args:
           client - nova client object

       Returns:
           none
    """
    print("\nList Instances: ")
    for line in client.servers.list():
        print(line)

def list_images(client):
    """
       Lists available images

       Args:
           client - nova client object

        Returns:
            none
    """
    print("\nList Images: ")
    for line in client.images.list():
        print(line)

def list_flavors(conn):
    """
       Lists available flavors

       Args:
           client - nova client object

        Returns:
            none
    """
    print("\nList Flavors: ")
    for line in client.flavors.list():
        print(line)

def list_networks(client):
    """
       Lists available networks

       Args:
           client - nova client object

        Returns:
            none
    """
    print("\nList Networks: ")
    for line in client.networks.list():
        print(line)

# Instance functions

def instance_hub(client):
    """
       Menu for instance related functions
    """
    while(True):
        print("\nBackend Instance Functions")
        print("1. Create Instance")
        print("2. Terminate Instance")
        print("3. Rename Instance")
        print("4. Return to Main Menu")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            create_instance(client)
        elif case == 2:
            terminate_instance(client)
        elif case == 3:
            rename_instance(client)
        elif case == 4:
            return
        else:
            print("\nInvalid option")
    

def create_instance(client):
    """
       Creates an instance of given name, image and flavor

       Args:
           name_in - name of new instance
           img_in - name of image to use
           flav_in - name of flavor to use

        Returns:
            none
    """
    try:
        name_in = input("Enter instance name: ")
        img_in = input("Enter image to use: ")
        image = client.images.find(name=img_in)
        flav_in = input("Enter flavor: ")
        flavor = client.flavors.find(name=flav_in)
        net = client.networks.find(label="Shared")
        nics = [{'net-id': net.id}]
        instance = client.servers.create(name=name_in,
                                         image=image,
                                         flavor=flavor,
                                         nics=nics)
        time.sleep(5)
    finally:
        print("Instance Created")

def terminate_instance(client):
    """
       Terminates an instance of given name

       Args:
          name_in - name of instance to terminate

       Returns:
          None
    """
    servers_list = client.servers.list()
    name_in = input("Enter instance name: ")
    server_exists = False

    for s in servers_list:
        if s.name == name_in:
            server_exists = True
            break
    if not server_exists:
        print("%s does not exist" % name_in)
    else:
        print("Deleting %s" % name_in)
        client.servers.delete(s)

def rename_instance(client):
    """
       TODO: implement

       Renames an existing instance of given name with new name

       Args:
          name_in - name of existing instance
          new_name - new name for instance

       Returns:
          None
    """
    servers_list = client.servers.list()
    name_in = input("Enter instance name: ")
    server_exists = False

    for s in servers_list:
        if s.name == name_in:
            server = client.servers.get(s.id)
            server_exists = True
            break
    if not server_exists:
        print("%s does not exist" % name_in)
    else:
        print("Renaming %s" % name_in)
        new_name = input("Enter new name for instance: ")
        server.update(server=new_name)

# Web functions

def create_dirauth(client,img,flav,net,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "directory_authority" + str(i)
            if img is None:
                img = client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i = 0:
                    logger(None,None,"Directory Authority: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = client.flavors.find(name="m1.tiny")
                if i = 0:
                    logger(None,None,"Directory Authority: No flavor specified, defaulting to m1.tiny",None)                
            if net is None:
                net = client.networks.find(label="Shared")
                if i = 0:
                    logger(None,None,"Directory Authority: No network specified, defaulting to Shared",None)
            nics = [{'net-id': net.id}]
            instance = client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "directory authorities created",None,None)

def create_guardnode(client,img,flav,net,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "guard_node" + str(i)
            if img is None:
                img = client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i = 0:
                    logger(None,None,"Guard node: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = client.flavors.find(name="m1.tiny")
                if i = 0:
                    logger(None,None,"Guard node: No flavor specified, defaulting to m1.tiny",None)                
            if net is None:
                net = client.networks.find(label="Shared")
                if i = 0:
                    logger(None,None,"Guard node: No network specified, defaulting to Shared",None)
            nics = [{'net-id': net.id}]
            instance = client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "guard nodes created",None,None)

def create_exitnode(client,img,flav,net,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "exit_node" + str(i)
            if img is None:
                img = client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i = 0:
                    logger(None,None,"Exit node: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = client.flavors.find(name="m1.tiny")
                if i = 0:
                    logger(None,None,"Exit node: No flavor specified, defaulting to m1.tiny",None)                
            if net is None:
                net = client.networks.find(label="Shared")
                if i = 0:
                    logger(None,None,"Exit node: No network specified, defaulting to Shared",None)
            nics = [{'net-id': net.id}]
            instance = client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "exit nodes created",None,None)

def create_relaynode(client,img,flav,net,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "relay_node" + str(i)
            if img is None:
                img = client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i = 0:
                    logger(None,None,"Relay node: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = client.flavors.find(name="m1.tiny")
                if i = 0:
                    logger(None,None,"Relay node: No flavor specified, defaulting to m1.tiny",None)
            if net is None:
                net = client.networks.find(label="Shared")
                if i = 0:
                    logger(None,None,"Relay node: No network specified, defaulting to Shared",None)
            nics = [{'net-id': net.id}]
            instance = client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "relay nodes created",None,None)
    
# Launch functions

def web_launch(username,password,img,flav,net,size):
    client = create_connection(username,password)
    logger("Client initialized by " + username + " from web UI","Starting new network build of size " + str(size),None,None)
    # TODO make config dictionary
    create_dirauth(client,config)
    create_guardnode(client,config)
    create_exitnode(client,config)
    create_relaynode(client,config)

if __name__ == '__main__':
    client = create_connection(None,None)
    while(True):
        print("\nOpenstack SDK Backend - Main Menu")
        print("1. Reporting Options")
        print("2. Instance Options")
        print("3. Exit")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            list_hub(client)
        elif case == 2:
            instance_hub(client)
        elif case == 3:
            print("Goodbye")
            exit()
        else:
            print("\nInvalid option")
