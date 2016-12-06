"""
   file: launch.py
   vers: 2.0
   desc: Openstack Tor Network builder backend
"""

import time
import getpass
import logging
from novaclient.client import Client

# global variables

debug_on = False
num_nodes = 0

# Logging functions

def logger(session, alert, bug, err):
    """
        Logs session, alert, debug and error to log file

        Args (strings):
            session - session log message
            alert - alert log message
            bug - bug log message
            err - error log message
    """
    timestamp = time.strftime("%m%d%Y")
    logtime = time.strftime(" %H:%M.%S ")
    fn = "tor_net_" + timestamp + ".log"
    logging.basicConfig(filename=fn, filemode='a', level=logging.DEBUG)

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

def get_auth(username, password):
    """
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
    global project_id, auth_url, auth_vers, ssl_setting

    username = username + "@ad.rit.edu"
    auth = {}
    auth['version'] = auth_vers
    auth['insecure'] = True
    auth['username'] = username
    auth['password'] = password
    auth['auth_url'] = auth_url
    auth['project_id'] = project_id
    if auth['insecure'] == ssl_setting:
        cert_warn = "Connection: SSL certificates being ignored"
        logger(None, cert_warn, cert_warn, None)
    return auth

def toggle_debug():
    """
        Sets a flag for debugging, if True logs will be sent to the
        debug message log file.
    """
    global debug_on
    if not debug_on:
        debug_on = True
        print("Debugging on, see log file")
    else:
        debug_on = False
        print("Debugging off")

# Network config functions

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
        logger("Nova client initialized by " + username + " from command line", None, None, None)
    auth = get_auth(username, password)
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
           nova_client - instance of Openstack Nova Client object

        Returns:
            None
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
                                              nics=nics,
                                              userdata=launch_script)
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

def create_utilserv(nova_client, util_config, override_size):
    util_config['name'] = "util_serv"
    if override_size is not None:
        util_config['size'] = override_size
    else:
        util_config['size'] = 1
    global num_nodes
    num_nodes = num_nodes - 1
    util_list = create_node(nova_client, util_config)

    return util_list

def create_hiddenservice(nova_client, hs_config, override_size):
    hs_config['name'] = "hidden_service"
    if override_size is not None:
        hs_config['size'] = override_size
    else:
        hs_config['size'] = 1
    hs_config['script'] = load_launch_script("HS", hs_config['util_ip'])
    hs_list = create_node(nova_client, hs_config)

    return hs_list

def create_dirauth(nova_client, da_config, override_size):
    da_config['name'] = "dir_auth"
    if override_size is not None:
        da_config['size'] = override_size
    else:
        da_config['size'] = da_config['da_size']
    da_config['script'] = load_launch_script("DA", da_config['util_ip'])

    global num_nodes
    num_nodes = num_nodes - da_config['da_size']
    da_list = create_node(nova_client,da_config)

    return da_list

def create_exitnode(nova_client, exit_config, override_size):
    exit_config['name'] = "exit_node"
    exit_config['script'] = load_launch_script("EXIT", exit_config['util_ip'])
    if override_size is not None:
        exit_config['size'] = override_size
    else:
        global num_nodes
        n_size = int(num_nodes / 3)
        num_nodes = num_nodes - n_size
        exit_config['size'] = n_size
    exit_list = create_node(nova_client,exit_config)

    return exit_list

def create_relaynode(nova_client, relay_config, override_size):
    relay_config['name'] = "relay_node"
    relay_config['script'] = load_launch_script("RELAY", relay_config['util_ip'])
    if override_size is not None:
        relay_config['size'] = override_size
    else:
        global num_nodes
        n_size = int(num_nodes / 2)
        num_nodes = num_nodes - n_size
        relay_config['size'] = n_size
    relay_list = create_node(nova_client,relay_config)

    return relay_list

def create_clientnode(nova_client, client_config, overide_size):
    client_config['name'] = "client_node"
    client_config['script'] = load_launch_script("CLIENT", client_config['util_ip'])
    if override_size is not None:
        client_config['size'] = override_size
    else:
        global num_nodes
        n_size = int(num_nodes)
        num_nodes = num_nodes - n_size
        if num_nodes > 0:
            n_size = n_size + 1
        client_config['size'] = n_size
    client_list = create_node(nova_client, client_config)

    return client_list

def create_node(nova_client, config):
    """
        TODO: add error checking

        Helper function to create instances.

        Args:
            nova_client - instance of the client connection to Openstack
            config - dictionary containing parameters:
                        * image - name of image to use
                        * flavor - name of flavor to use
                        * netname - name of network to use
                        * script - name of launch script to use
                        * size - number of elements to create

        Returns:
            client_list - a list of client objects created
    """
    global default_image, default_flavor, default_network, launch_script

    node_list = []
    image = config['image']
    flavor = config['flavor']
    netname = config['netname']
    size = config['size']
    node_name = config['name']
    util_ip = config['util_ip']

    if image is None:
        image = nova_client.images.find(name=default_image)
    if flavor is None:
        flavor = nova_client.flavors.find(name=default_flavor)
    if netname is None:
        netname = nova_client.networks.find(label=default_network)
    nics = [{'net-id': netname.id}]

    for i in range(0,size):
        name = node_name + str(i)
        instance = nova_client.servers.create(name=name,
                                              image=image,
                                              flavor=flavor,
                                              nics=nics,
                                              userdata=config['script'])
        node_list.append(instance)
        time.sleep(5)
        logger(None, "Network: " + name + " node created", None, None)

    return node_list

# File modifiers

def load_launch_script(node_type, util_ip):
    """
        Modifies deploy.sh script to include correct node type and
        utility server IP.

        Args:
            node_type - type of node being created
            util_ip - IP address of the utility server

        Returns:
            deploy_script - a string value containing the script to run at launch
    """
    load_config_file()
    global launch_script
    try:
        with open(launch_script,'r') as script:
            lines = []
            for line in script:
                lines.append(line)
        script.close()
    except:
        err_msg = "Dependency error: Missing node launch script"
        logger(None, None, err_msg, err_msg)
    deploy_script = ""
    for line in lines:
        if "ROLE=" in line:
            deploy_script = deploy_script + "ROLE=" + node_type + '\n'
        elif "UTIL_SERVER=" in line:
            deploy_script = deploy_script + "UTIL_SERVER=" + str(util_ip) + '\n'
        else:
            deploy_script = deploy_script + line

    return deploy_script

def load_config_file():
    """
        Loads parameters from the torlaunch.conf file

        Args:
            None

        Returns:
            None
    """
    global project_id, auth_url, auth_vers, ssl_setting, default_image, default_flavor, default_network, launch_script
    try:
        with open('torlaunch.conf','r') as config:
            for line in config:
                if "project_name" in line:
                    spline = line.split(' ')
                    try:
                        project_id = spline[1]
                    except:
                        err_msg = "Config error: No value specified for project_name"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            project_id = project_id + " " + spline[i]
                    project_id = project_id.strip()

                elif "authentication_url" in line:
                    spline = line.split(' ')
                    try:
                        auth_url = spline[1]
                    except:
                        err_msg = "Config error: No value specified for authentication_url"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            auth_url = auth_url + " " + spline[i]
                    auth_url = auth_url.strip()

                elif "authentication_version" in line:
                    spline = line.split(' ')
                    try:
                        auth_vers = spline[1]
                    except:
                        err_msg = "Config error: No value specified for authentication_version"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            auth_vers = auth_vers + " " + spline[i]
                    auth_vers = auth_vers.strip()

                elif "ssl_cert_warnings" in line:
                    spline = line.split(' ')
                    try:
                        ssl_setting = spline[1]
                    except:
                        err_msg = "Config error: No value specified for ssl_cert_warnings"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            ssl_setting = ssl_setting + " " + spline[i]
                    if ssl_setting is "disabled":
                        ssl_setting = True
                    else:
                        ssl_setting = False

                elif "default_image" in line:
                    spline = line.split(' ')
                    try:
                        default_image = spline[1]
                    except:
                        err_msg = "Config error: No value specified for default_image"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            default_image = default_image + " " + spline[i]
                    default_image = default_image.strip()

                elif "default_flavor" in line:
                    spline = line.split(' ')
                    try:
                        default_flavor = spline[1]
                    except:
                        err_msg = "Config error: No value specified for default_flavor"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            default_flavor = default_flavor + " " + spline[i]
                    default_flavor = default_flavor.strip()

                elif "default_network" in line:
                    spline = line.split(' ')
                    try:
                        default_network = spline[1]
                    except:
                        err_msg = "Config error: No value specified for default_network"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            default_network = default_network + " " + spline[i]
                    default_network = default_network.strip()

                elif "node_launch_script" in line:
                    spline = line.split(' ')
                    try:
                        launch_script = spline[1]
                    except:
                        err_msg = "Config error: No value specified for node_launch_script"
                        logger(None, None, err_msg, err_msg)
                    if len(spline) > 2:
                        for i in range(2, len(spline)):
                            launch_script = launch_script + " " + spline[i]
                    launch_script = launch_script.strip()

                else:
                    pass
        config.close()

    except:
        err_msg = "Tried to load torlaunch.conf but no config file was found"
        logger(None, None, err_msg, err_msg)

# Teardown functions

def destroy_network(nova_client, node_list):
    """
        Deletes nodes by id.

        Args:
            nova_client - instance of Openstack Nova Client object
            node_list - list of nodes to be removed

        Returns:
            None
	"""
    for key in node_list:
        for e in node_list[key]:
            nova_client.servers.delete(e.id)

# Launch functions

def web_launch(nova_client, img, flav, netname, util_ip, size, da_size):
    """
        Called directly from the web interface. Creates nodes in the correct order
        and returns a list of new nodes ot the web interface.

        Args:
            nova_client - instance of Openstack Nova client object
            netname - name of network to use
            util_ip - IP address of the utility server
            size - size of network to create
            da_size - number of directory authorities to create

        Returns:
            nodes - a dictionary of lists containing the newly created nodes
    """
    load_config_file()
    logger("Nova client initialized from web UI",None, None, None)
    logger("Starting new network build of size " + str(size),None, None, None)

    config = {'image': img,
	          'flavor': flav,
	          'netname': netname,
              'util_ip': util_ip,
              'size': size,
              'da_size': da_size}

    global num_nodes
    num_nodes = config['size']

    da_list = create_dirauth(nova_client, config, None)
    exit_list = create_exitnode(nova_client, config, None)
    relay_list = create_relaynode(nova_client, config, None)
    client_list = create_clientnode(nova_client, config, None)

    nodes = {'client': client_list,
             'relay': relay_list,
             'exit': exit_list,
             'da': da_list}

    return nodes

def web_dismantle(nova_client, node_list):
    """
        Called directly from the web interface. Destroys nodes in provided list

        Args:
            nova_client - instance of Openstack Nova client object
            node_list - list of nodes to destroy

        Returns:
            None
    """
    destroy_network(nova_client, node_list)

# Test functions

def test_launch(username, password, img, flav, netname, util_ip, size, da_size):
    """
        tests network launch
    """
    nova_client = create_novaclient(username,password)

    config = {'image': img,
	          'flavor': flav,
	          'netname': netname,
	          'util_ip': util_ip,
	          'size': size,
              'da_size': da_size}

    global num_nodes
    num_nodes = config['size']

    util_list = create_utilserv(nova_client, config)
    da_list = create_dirauth(nova_client, config)
    exit_list = create_exitnode(nova_client, config)
    relay_list = create_relaynode(nova_client, config)
    client_list = create_clientnode(nova_client, config)
    nodes = {'client': client_list,
             'relay': relay_list,
             'exit': exit_list,
             'da': da_list,
             'util': util_list}

    return nodes

# Main

if __name__ == '__main__':
    load_config_file()
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
