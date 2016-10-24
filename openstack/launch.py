"""
   file: launch.py
   desc: Openstack Tor Network builder backend
"""

import time
import getpass
from novaclient.client import Client

# Connection functions

def get_auth():
    """
       Dictionary for user authentication parameters

       Args:
           none

       Returns:
           auth - dictionary for authenticating to openstack keyauth
    """
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    username = username + "@ad.rit.edu"
    auth = {}
    auth['version'] = '2'
    auth['insecure'] = True
    auth['username'] = username
    auth['password'] = password
    auth['auth_url'] = 'https://acopenstack.rit.edu:5000/v2.0'
    auth['project_id'] = 'jrh7130-multi'
    return auth

def create_connection():
    """
        Creates a nova client with given authentication parameters

        Args:
           none

        Returns:
           nova_client - object to query openstack
    """
    auth = get_auth()
    nova_client = Client(**auth)
    return nova_client

# List functions

def list_hub(client):
    """
       Menu for reporting related functions
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
        print("\nBackend Create Functions")
        print("1. Create Instance")
        print("2. Return to Main Menu")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            create_instance(client)
        elif case == 2:
            return
        else:
            print("\nInvalid option")
    

def create_instance(client):
    """
       Creates an instance with given specs

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
        instance = client.servers.create(name=name_in, image=image,
                                      flavor=flavor, nics=nics)
        time.sleep(5)
    finally:
        print("Instance Created")
    

if __name__ == '__main__':
    client = create_connection()
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
