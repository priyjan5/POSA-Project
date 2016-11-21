import tkinter
import getpass
from launch import test_launch, web_dismantle

if __name__ == '__main__':
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    print("Spawning instances, please wait")
    nodes = test_launch(username,password,None,None,None,None,2)
    for key in nodes:
        print(nodes[key])
    cn = input("Press Enter to continue")
    web_dismantle(username,password,nodes)
    
