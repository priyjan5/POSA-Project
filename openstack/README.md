# Openstack Tor Project

## Version
- Python 3.5.2
- Pip 8.1.2

## Dependencies
- python-openstackclient

## Imports
- time
- getpass
- from novaclient.client import Client

## Functions
### Lists
- list_servers
  * Lists running instances

- list_images
  * Lists available images

- list_flavors
  * Lists available flavors

- list_networks
  * Lists available networks

### Creates
- create_instance
  * Creates a new instance based on given options
  
## Reference
- http://docs.openstack.org/developer/python-novaclient/ref/v2/client.html
- http://docs.openstack.org/user-guide/sdk-compute-apis.html#create-server-api-v2
