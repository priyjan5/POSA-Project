# Openstack Tor Project

## Versions
- Python 3.5.2
- Pip 8.1.2

## Considerations
- Version 1.4: SSL Certificates are being ignored

## Dependencies
- python-openstackclient

## Imports
- import time
- import getpass
- import logging
- from novaclient.client import Client

## Guide

To use the Tor network builder script use 'from launch import web_launch'
This script takes the listed parameters and creates a Tor network of the 
listed nodes. The web launch function will return a dictionary of lists
containing the newly created nodes.

## Web UI Functions
### Launch
- web_launch: Launches build functions for a new Tor network
  * Parameters: 
    * nova_clinet: Openstack Nova client object
	* img: Specifies which image to use
	* flav: Specifies which flavor to use
	* netname: Specifies which network to use
	* modifier: Specifies which userdata script to use
	* size: Total size of network being created
	* num_das: Specifies number of directory authorities to create
  * Returns:
	* nodes: A dictionary of lists creating references to the new nodes
	
### Teardown
- web_dismantle: Destroys nodes
  * Paramters:
	* nova_client: Openstack Nova client object
	* node_list: List of nodes to be terminated
	
## Command-line Functions
### Reporting
- list_servers
  * Lists running instances
- list_images
  * Lists available images
- list_flavors
  * Lists available flavors
- list_networks
  * Lists available networks

### Instances
- create_instance
  * Creates a new instance based on given name, image, flavor
- terminate_instance 
  * Terminates an instance based on given name
  
## TODO
- Add JSON input support
- Make instance creation more configurable
- Add support for updating instances post-creation
  
## Reference
- http://docs.openstack.org/developer/python-novaclient/ref/v2/client.html
- http://docs.openstack.org/user-guide/sdk-compute-apis.html#create-server-api-v2
