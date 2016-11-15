import tkinter
import getpass
from launch import test_launch

if __name__ == '__main__':
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    nodes = test_launch(username,password,None,None,None,None,5)
    for key in nodes:
        print(nodes[key])