"""
   file: launch.py
   vers: 1.6
   desc: Openstack Tor Network builder backend
"""

import time
import getpass
import logging
from novaclient.client import Client

networks = {}
debug_on = False

# Logging functions

def logger(alert,session,bug,err):
    timestamp = time.strftime("%m%d%Y")
    logtime = time.strftime(" %H:%M.%S ")
    fn = "tor_net_" + timestamp + ".log"
    logging.basicConfig(filename=fn, filemode='a', level=logging.DEBUG)
    """
       TODO: implement
    """
    if alert is not None:
        logging.warn(logtime + alert)
    if session is not None:
        logging.info(logtime + session)
    if bug is not None:
        if debug_on:
            logging.debug(logtime + bug)
    if err is not None:
        logging.error(logtime + err)

# Connection functions

def get_auth(username,password):
    """
       TODO: remove hardcoded variables

       Dictionary for user authentication parameters

       Function of:
           create_novaclient
           create_neutronclient

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
    if auth['insecure'] == True:
        cert_warn = "Connection: SSL certificates being ignored"
        logger(cert_warn,None,cert_warn,None)
    return auth

def toggle_debug():
    if not debug_on:
        debug_on = True
        print("Debugging on, see log file")
    else:
        debug_on = False
        print("Debugging off")

# Network config functions

def net_builder(node_type,name,netname):
    """
       TODO: delete
    
       Internal helper function to maintain network configuration
    """
    if netname is not None:
        if netname not in networks:
            networks[netname] = {"nodes":[]}
    if netname is None:
        networks["Shared"] = {"nodes":[]}
        netname = "Shared"
    networks[netname][node_type].append(name)

def create_novaclient(username,password):
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
        logger("Nova client initialized by " + username + " from command line",None,None,None)
    auth = get_auth(username,password)
    nova_client = Client(**auth)
    return nova_client

# List functions

def list_hub(nova_client):
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
            list_instances(nova_client)
        elif case == 2:
            list_images(nova_client)
        elif case == 3:
            list_flavors(nova_client)
        elif case ==4:
            list_networks(nova_client)
        elif case == 5:
            return
        else:
            print("\nInvalid option")

def list_instances(nova_client):
    """
       Lists available instances

       Args:
           client - nova client object

       Returns:
           none
    """
    print("\nList Instances: ")
    for line in nova_client.servers.list():
        print(line)

def list_images(nova_client):
    """
       Lists available images

       Args:
           client - nova client object

        Returns:
            none
    """
    print("\nList Images: ")
    for line in nova_client.images.list():
        print(line)

def list_flavors(nova_client):
    """
       Lists available flavors

       Args:
           client - nova client object

        Returns:
            none
    """
    print("\nList Flavors: ")
    for line in nova_client.flavors.list():
        print(line)

def list_networks(nova_client):
    """
       Lists available networks

       Args:
           client - nova client object

        Returns:
            nets - a list of networks
    """
    print("\nList Networks: ")
    nets = []
    for line in nova_client.networks.list():
        print(line)
        nets.append(line)
    return nets

# Instance functions

def instance_hub(nova_client):
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
            create_instance(nova_client)
        elif case == 2:
            terminate_instance(nova_client)
        elif case == 3:
            rename_instance(nova_client)
        elif case == 4:
            return
        else:
            print("\nInvalid option")
    

def create_instance(nova_client):
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
        image = nova_client.images.find(name=img_in)
        flav_in = input("Enter flavor: ")
        flavor = nova_client.flavors.find(name=flav_in)
        net = nova_client.networks.find(label="Shared")
        nics = [{'net-id': net.id}]
        instance = nova_client.servers.create(name=name_in,
                                              image=image,
                                              flavor=flavor,
                                              nics=nics)
        time.sleep(5)
    finally:
        print("Instance Created")

def terminate_instance(nova_client):
    """
       Terminates an instance of given name

       Args:
          name_in - name of instance to terminate

       Returns:
          None
    """
    servers_list = nova_client.servers.list()
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
        nova_client.servers.delete(s)

def rename_instance(nova_client):
    """
       TODO: implement

       Renames an existing instance of given name with new name

       Args:
          name_in - name of existing instance
          new_name - new name for instance

       Returns:
          None
    """
    servers_list = nova_client.servers.list()
    name_in = input("Enter instance name: ")
    server_exists = False

    for s in servers_list:
        if s.name == name_in:
            server = nova_client.servers.get(s.id)
            server_exists = True
            break
    if not server_exists:
        print("%s does not exist" % name_in)
    else:
        print("Renaming %s" % name_in)
        new_name = input("Enter new name for instance: ")
        server.update(server=new_name)

# Web functions

def create_dirauth(nova_client,img,flav,netname,modifier,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "directory_authority" + str(i)
            if img is None:
                img = nova_client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i == 0:
                    logger(None,None,"Directory Authority: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = nova_client.flavors.find(name="m1.tiny")
                if i == 0:
                    logger(None,None,"Directory Authority: No flavor specified, defaulting to m1.tiny",None)                
            if netname is None:
                netname = nova_client.networks.find(label="Shared")
                if i == 0:
                    logger(None,None,"Directory Authority: No network specified, defaulting to Shared",None)
            nics = [{'net-id': netname.id}]
            instance = nova_client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics,
                                             userdata=modifier)
            net_builder("directory",name,netname)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "directory authorities created",None,None)

def create_exitnode(nova_client,img,flav,netname,modifier,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "exit_node" + str(i)
            if img is None:
                img = nova_client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i == 0:
                    logger(None,None,"Exit node: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = nova_client.flavors.find(name="m1.tiny")
                if i == 0:
                    logger(None,None,"Exit node: No flavor specified, defaulting to m1.tiny",None)                
            if netname is None:
                netname = nova_client.networks.find(label="Shared")
                if i == 0:
                    logger(None,None,"Exit node: No network specified, defaulting to Shared",None)
            nics = [{'net-id': netname.id}]
            instance = nova_client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics,
                                             userdata=modifier)
            net_builder("exit",name,netname)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "exit nodes created",None,None)

def create_relaynode(nova_client,img,flav,netname,modifier,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "relay_node" + str(i)
            if img is None:
                img = nova_client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i == 0:
                    logger(None,None,"Relay node: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = nova_client.flavors.find(name="m1.tiny")
                if i == 0:
                    logger(None,None,"Relay node: No flavor specified, defaulting to m1.tiny",None)
            if netname is None:
                netname = nova_client.networks.find(label="Shared")
                if i == 0:
                    logger(None,None,"Relay node: No network specified, defaulting to Shared",None)
            nics = [{'net-id': netname.id}]
            instance = nova_client.servers.create(name=name,
                                             image=image,
                                             flavor=flavor,
                                             nics=nics,
                                             userdata=modifier)
            net_builder("relay",name,netname)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "relay nodes created",None,None)

def create_clientnode(nova_client,img,flav,netname,modifier,size):
    """
       TODO: implement, add error catching
    """
    try:
        for i in range(0,size):
            name = "client_node" + str(i)
            if img is None:
                img = nova_client.images.find(name="Ubuntu 14.04.4 Fresh Install")
                if i == 0:
                    logger(None,None,"Client node: No image name provided, defaulting to Ubuntu 14.04.4",None)
            if flav is None:
                flav = nova_client.flavors.find(name="m1.tiny")
                if i == 0:
                    logger(None,None,"Client node: No flavor specified, defaulting to m1.tiny",None)
            if netname is None:
                netname = nova_client.networks.find(label="Shared")
                if i == 0:
                    logger(None,None,"Client node: No network specified, defaulting to Shared",None)
            nics = [{'net-id': netname.id}]
            instance = nova_client.servers.create(name=name,
                                                  image=image,
                                                  flavor=flavor,
                                                  nics=nics,
                                                  userdata=modifier)
            net_builder("client",name,netname)
            time.sleep(5)
    finally:
        logger(None,"Network: " + str(size) + "client nodes created",None,None)

# Teardown functions

def destroy_network(nova_client,netname):
    for e in networks[netname][nodes]:
        logger("Deleting " + netname,"Network: Deleting node " + e,None,None)
        nova_client.servers.delete(e)
        
    
# Launch functions

def web_launch(username,password,netname,modifier,size):
    nova_client = create_novaclient(username,password)
    logger("Nova client initialized by " + username + " from web UI","Starting new network build of size " + str(size),None,None)
    create_dirauth(nova_client,config)
    create_exitnode(nova_client,config)
    create_relaynode(nova_client,config)

if __name__ == '__main__':
    nova_client = create_novaclient(None,None)
    while(True):
        print("\nOpenstack SDK Backend - Main Menu")
        print("1. Reporting Options")
        print("2. Instance Options")
        print("3. Toggle debug")
        print("4. Exit")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            list_hub(nova_client)
        elif case == 2:
            instance_hub(nova_client)
        elif case == 3:
            toggle_debug()
        elif case == 4:
            print("Goodbye")
            exit()
        else:
            print("\nInvalid option")
