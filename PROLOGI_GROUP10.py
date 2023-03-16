import json
from os import system

# this loads the external database, simulated by a json file.
accountDatabase = json.load(open('database.json', 'r'))

accountMatched = False

# repeat the login process while a valid username and password have not been entered yet.
while not accountMatched:
    print("\nPizza Ordering System")
    print("Please enter your username and password.")
    
    # prompts user for username and password.
    username = input("Username: ")
    password = input("Password: ")

    # checks input against database.
    for account in accountDatabase:
        currentAccount = accountDatabase[account]
        if username == currentAccount['username']:
            if password == currentAccount['password']:
                print("Welcome, " + username)
                accountMatched = True
                break

    if not accountMatched:
        system('cls')
        print("You have entered either an incorrect username or password.")

