import time
import getpass
from novaclient.client import Client

# Connection functions

def test():
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
    nova_client = Client(**auth)
    return nova_client

def get_auth():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    username = username + "@ad.rit.edu"
    auth = {}
    auth['verify'] = False
    auth['username'] = username
    auth['password'] = password
    auth['auth_url'] = 'https://acopenstack.rit.edu:5000/v2.0'
    auth['project_id'] = 'b4cac92e8b0147e29d1af5c3d05968de'
    return auth

def create_connection():
    auth = get_auth()
    conn = connection.Connection(**auth)
    return conn

# List functions

def list_hub(client):
    while(True):
        print("\nBackend List Functions")
        print("1. List Servers")
        print("2. List Images")
        print("3. List Flavors")
        print("4. List Networks")
        print("5. Return to Main Menu")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            list_servers(client)
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

def list_servers(client):
    print("List Servers: ")
    for line in client.servers.list():
        print(line)

def list_images(client):
    print("List Images: ")
    for line in client.images.list():
        print(line)

def list_flavors(conn):
    print("List Flavors: ")
    for line in client.flavors.list():
        print(line)

def list_networks(client):
    print("List Networks: ")
    for line in client.networks.list():
        print(line)

# Make functions

def create_hub(client):
    create_instance(client)

def create_instance(client):
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
        print("Sleeping for 5s after create command")
        print("List of VMs")
        time.sleep(5)
        print(client.servers.list())
    finally:
        print("Instance Created")
    

if __name__ == '__main__':
    client = test()
    while(True):
        print("\nOpenstack SDK Backend")
        print("1. Lists")
        print("2. Creates")
        print("3. Exit")
        try:
            case = int(input("Enter choice: "))
        except:
            case = 6
        if case == 1:
            list_hub(client)
        elif case == 2:
            create_hub(client)
        elif case == 3:
            print("Goodbye")
            exit()
        else:
            print("\nInvalid option")
