from launch import modify_script, load_config_file

if __name__ == '__main__':
    print("Testing load_config_file()")
    load_config_file()
    print("Testing modify_script()")
    print(modify_script("CLIENT","8.8.8.8"))
