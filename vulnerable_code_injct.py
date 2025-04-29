# vuln_example.py

import os

def run_command(user_input):
    # This is an example of OS command injection vulnerability
    os.system("echo " + user_input)

def main():
    user_data = input("Enter your name: ")
    run_command(user_data)

if __name__ == "__main__":
    main()
