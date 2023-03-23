import json
from os import system

# orders in both orderList and orderHistory are arrays that are structured as follows:
# Crust size,
# Toppings,
# Crust type,
# Crust stuffing,
# Price (float)
# Example: ["Small - 10 inch", "Pepperoni", "Thin crust", "Cheese stuffed crust", 469.00]
orderList = []

def addOrder():
    menuDatabase = json.load(open('menu.json', 'r'))
    page = 0
    
    # add en empty array to the order list and get the index in the list
    # this is to accommodate multiple orders.
    orderList.append([])
    orderIndex = len(orderList) - 1
    
    currentOrder = orderList[orderIndex]
    dividerLength = 130
    
    price = float("%0.2f" % menuDatabase['basePrice'])
    
    while page < 6:
        system('cls')
        # crust size
        if page == 0:
            print("| Order a Pizza \t\t | Php" + str(price) + "\t\t | [Crust Size] - Dough - Stuffing - Toppings - Review Order - Payment |")
            print("-" * dividerLength)
            output = selector(menuDatabase['sizes'])
            price += output[1]
            currentOrder.append(output[0])
            page += 1
            # toppings
        elif page == 1:
            print("| Order a Pizza \t\t | Php" + str(price) + "\t\t | Crust Size - [Dough] - Stuffing - Toppings - Review Order - Payment |")
            print("-" * dividerLength)
            output = selector(menuDatabase['toppings'])
            price += output[1]
            currentOrder.append(output[0])
            page += 1
        # dough
        elif page == 2:
            print("| Order a Pizza \t\t | Php" + str(price) + "\t\t | Crust Size - Dough - [Stuffing] - Toppings - Review Order - Payment |")
            print("-" * dividerLength)
            output = selector(menuDatabase['dough'])
            price += output[1]
            currentOrder.append(output[0])
            page += 1
        # stuffing
        elif page == 3:
            print("| Order a Pizza \t\t | Php" + str(price) + "\t\t | Crust Size - Dough - Stuffing - [Toppings] - Review Order - Payment |")
            print("-" * dividerLength)
            output = selector(menuDatabase['stuffing'])
            price += output[1]
            currentOrder.append(output[0])
            page += 1
        # review
        elif page == 4:
            print("| Order a Pizza \t\t | Php" + str(price) + "\t\t | Crust Size - Dough - Stuffing - Toppings - [Review Order] - Payment |")
            print("-" * dividerLength)
            print("\nYour pizza: ")
            for i in currentOrder:
                print(str(i))
            break
            

def selector(list, previousChoice = None):
    selectedChoice = None
    while selectedChoice == None:
        for item in list:
            index = list.index(item)
            if index % 3 == 0 and index != 0:
                print("\n")
            # prints the item number, the name of the item, and the price. 
            # it prints three items on one line, separated by an indent.
            # that's what the `end = "\t"` is for.
            print("(" + str(index) + ") " + "{0:<40}".format(item[0]) + " +Php" + str(item[1]), end = "\t\t")
        
        
        # we allow the user to go back to change their choice after the final step
        # this shows the user what they chose previously.
        if previousChoice != None:
            print(previousChoice)
        
        # if the user inputs a letter or an invalid number, keep the loop going.
        # otherwise, end the loop.
        try:
            choice = int(input("\n\nChoose an option: "))
            list[choice]
        except ValueError:
            print("Invalid choice")
        except IndexError:
            print("Invalid choice")
        else:
            selectedChoice = choice
    # output is an array containing the name and price of the choice.
    # Example: ["Small (10 inch)", 0.00]
    return list[selectedChoice]

def orderPageSelector():
    pass

# to create a seamless loop with the menu,
# all the functions below call the menu() function after running.
def payOrder(orderList):
    pass

def viewOrderHistory(orderHistory):
    if orderHistory == []:
        menu("You have not ordered anything.")
    
    print("Order History")
    print("This list is sorted from newest to oldest.")
    for order in reversed(orderHistory):
        print("(" + str(orderHistory.index(order)) + ")" + " " + order[0] + "\n    " + order[1] + "\n    " + order[2] + "\n    " + order[3] + "\n    Php " + str(order[4]))
    
    input("Press ENTER to go back to the main menu.")
    menu()

def viewCart(orderList):
    if orderList == []:
        menu("You have no items in your cart.")
    
    print("Cart")
    for order in orderList:
        print("(" + str(orderList.index(order)) + ")" + " " + order[0] + "\n    " + order[1] + "\n    " + order[2] + "\n    " + order[3] + "\n    Php " + str(order[4]))

# if you have to tell the user a message sa they go back to the menu, 
# call the menu() function with the message as a string parameter
def menu(message = None):
    system('cls')
    if message != None:
        print(message)
    
    print("Type a letter corresponding to your desired menu option.")
    print("(A)dd pizza to order - (P)ay for order - View order (h)istory - (Q)uit")
    
    chosenOption = input()
    system('cls')
    
    if chosenOption == 'a':
        addOrder()
    elif chosenOption == 'p':
        payOrder(orderList)
    elif chosenOption == 'h':
        viewOrderHistory(orderHistory)
    elif chosenOption == 'q':
        quit()

def quit():
    if orderList == []:
        print("Goodbye.")
        exit()
    
    userChoice = ""
    
    while userChoice != 'y' or userChoice != 'n':
        print("Your current orders will be discarded. Do you want to quit? (Y/N): ")
        userChoice = input().lower()
        
        if userChoice == 'y':
            system('cls')
            print("Goodbye.")
            accountDatabase.close()
            exit()
        elif userChoice == 'n':
            menu()
    

# this loads the external database, simulated by a json file.
accountDatabase = json.load(open('accounts.json', 'r'))

accountMatched = False

system('cls')

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
        if username == currentAccount['username'] and password == currentAccount['password']:
            system('cls')
            print("Welcome, " + username)
            orderHistory = currentAccount['orderHistory']
            accountMatched = True
            break

    system('cls')
    print("You have entered either an incorrect username or password.")

menu()