import json
from os import system, name

# orders in both orderList and orderHistory are arrays that are structured as follows:
# Crust size,
# Toppings,
# Crust type,
# Crust stuffing,
# Price (float)
# Example: ["Small - 10 inch", "Pepperoni", "Thin crust", "Cheese stuffed crust", 469.00]
orderList = []
menuJSON = open('menu.json', 'r')
menuDatabase = json.load(menuJSON)

# cross-platform screen clear.
# @mohit_negi. (2018, April). How to clear screen in python. https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # macos + linux
    else:
        _ = system('clear')

def addOrder(orderNumber = None):
    page = 0
    
    # this allows the user to edit a previous order
    if orderNumber != None:
        currentOrder = orderList[orderNumber]
    else:
        # add an array with placeholder values to the order list and get the index in the list
        # this is to accommodate multiple orders.
        orderList.append([None, None, None, None, None])
        
        # set current order to the last one in the list (.append() adds an item to the end of a list)
        currentOrder = orderList[-1]
    
    # number of dashes between the price/order ui on top and the menu
    dividerLength = 130
    
    # initialize the price with the base price as defined in the dictionary
    price = menuDatabase['basePrice']
    
    while page < 6:
        system('cls')
        print(str(orderList))
        
        # shows the user what their order is so far
        print("| Current pizza:", end = " ")
        for part in currentOrder:
            if part != None:
                print(part, end = " ")
        
        # prints first half of the second menu row
        print("|\n| Menu \t\t | Php " + "{0:.2f}".format(price), end = "\t\t")
        # crust size
        if page == 0:
            print("| [1. Crust Size] - 2. Dough - 3. Stuffing - 4. Toppings - 5. Review Order |")
            print("-" * dividerLength)
            output = selector(menuDatabase['sizes'])
        # toppings
        elif page == 1:
            print("| 1. Crust Size - [2. Dough] - 3. Stuffing - 4. Toppings - 5. Review Order |")
            print("-" * dividerLength)
            output = selector(menuDatabase['toppings'])
        # dough
        elif page == 2:
            print("| 1. Crust Size - 2. Dough - [3. Stuffing] - 4. Toppings - 5. Review Order |")
            print("-" * dividerLength)
            output = selector(menuDatabase['dough'])
        # stuffing
        elif page == 3:
            print("| 1. Crust Size - 2. Dough - 3. Stuffing - [4. Toppings] - 5. Review Order |")
            print("-" * dividerLength)
            output = selector(menuDatabase['stuffing'])
        # review
        elif page == 4:
            print("| 1. Crust Size - 2. Dough - 3. Stuffing - 4. Toppings - [5. Review Order] |")
            print("-" * dividerLength)
            currentOrder[page] = price
        else:
            menu("Item successfully added to your cart.")
                
        price += output[1]
        
        # page 4 has a different procedure
        if page < 4:
            currentOrder[page] = output[0]
        
        page += orderPageSelector(page)

# this function accepts a list of items to display.
# for example, if you pass menuDatabase['sizes'] to it,
# it will output small, medium, and large.
def selector(list):
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

        # if the user inputs a letter or an invalid number, keep the loop going.
        # otherwise, end the loop.
        try:
            choice = int(input("\n\nChoose an option: "))
            list[choice]
        except ValueError:
            print("Invalid choice. Please input a number from 0 to " + str(list.index(list[-1])))
        except IndexError:
            print("Invalid choice. Please input a number from 0 to " + str(list.index(list[-1])))
        else:
            selectedChoice = choice
    # output is an array containing the name and price of the choice.
    # Example: ["Small (10 inch)", 0.00]
    return list[selectedChoice]

# orderPageSelector() return either 1 or -1 if the user wants to go to the next page or the previous one.
# we can add that to the current page value to change the page.
def orderPageSelector(page):
    selectedChoice = None
    if page == 0:
        return 1
    elif page == 4:
        while selectedChoice == None:
            choice = input("Please ensure that all the items you have chosen so far are correct. Would you like to go back to the menu? (N to go back to the menu, P to go to the previous page): ").lower()
            if choice == 'n':
                menu()
            elif choice == 'p':
                return -1

            print("Invalid choice. Please input either 'n' or 'p'.")

    while selectedChoice == None:
        choice = input("Would you like to go to the next page or the previous page? (N for next, P for previous): ").lower()
        if choice == 'n':
            return 1
        elif choice == 'p':
            return -1

        print("Invalid choice. Please input either 'n' or 'p'.")

# to create a seamless loop with the menu,
# all the functions below call the menu() function after running.
def payOrder(orderList):    
    totalPrice = 0
    
    # calculate total price across all orders.
    for order in orderList:
        totalPrice += order[-1]
    
    print(str("{0:.2f}".format(totalPrice)))
    input()
    menu()

def viewOrderHistory(orderHistory):
    if orderHistory == []:
        menu("You have not ordered anything.")
    
    print("| Order History |")
    print("| This list is sorted from newest to oldest. |")
    print("----------------------------------------------")
    
    # .index() gets the first item that matches the given parameter,
    # meaning that duplicate items would break the system.
    orderNumber = len(orderHistory)
    for order in reversed(orderHistory):
        orderNumber -= 1
        # print a number that represents the order number. then, print each individual element of the order 
        print("(" + str(orderNumber) + ")" + " " + order[0] + "\n" + " " * (orderNumber + 4) + order[1] + "\n" + " " * (orderNumber + 4) + order[2] + "\n" + " " * (orderNumber + 4) + order[3] + "\n" + " " * (orderNumber + 4) + "Php " + str("{0:.2f}".format(order[4])))
    
    input("Press ENTER to go back to the main menu.")
    menu()

def viewCart(orderList):
    if orderList == []:
        menu("You have no items in your cart.")
    
    print("| View your cart |")
    print("| This list is sorted from newest to oldest. |")
    print("----------------------------------------------")
    
    orderNumber = len(orderList)
    for order in reversed(orderList):
        orderNumber -= 1
        # print a number that represents the order number. then, print each individual element of the order 
        print("(" + str(orderNumber) + ")" + " " + order[0] + "\n" + " " * (orderNumber + 4) + order[1] + "\n" + " " * (orderNumber + 4) + order[2] + "\n" + " " * (orderNumber + 4) + order[3] + "\n" + " " * (orderNumber + 4) + "Php " + str("{0:.2f}".format(order[4])))
    
    selectedChoice = None
    
    while selectedChoice == None:
        try:
            choice = input("Type the number of the order you would like to modify or press M to go back to the main menu: ")
            if choice == 'm' or choice == 'M':
                menu()
                break
            orderList[int(choice)]
        except ValueError:
            print("Invalid choice.")
        except IndexError:
            print("Invalid choice. That item is not in your cart.")
        except TypeError:
            print("Invalid choice.")
        else:
            selectedChoice = int(choice)
    
    clear()
    
    selectedOrder = orderList[selectedChoice]
    print("| View your cart | You are editing order " + str(orderNumber) + ". |")
    print("(" + str(orderNumber) + ")" + " " + selectedOrder[0])
    for part in selectedOrder[1:]:
        print(" " * (orderNumber + 4) + str(part))
    
    choice = input("Press E to edit the order, D to delete it, or M to go back: ").lower()
    if choice == 'e':
        addOrder(orderNumber)
    elif choice == 'd':
        orderList.pop(orderNumber)
        clear()
        print("Order " + str(orderNumber) + " removed.")
        viewCart(orderList)
    elif choice == 'm':
        clear()
        viewCart(orderList)
    menu()
        
        
# if you have to tell the user a message sa they go back to the menu, 
# call the menu() function with the message as a string parameter
def menu(message = None):
    clear()
    if message != None:
        print(message)
    
    print("Type a letter corresponding to your desired menu option.")
    print("(A)dd pizza to order - (P)ay for order - View (C)art - View order (h)istory - (Q)uit")
    
    chosenOption = input().lower()
    clear()
    
    if chosenOption == 'a':
        addOrder()
    elif chosenOption == 'p':
        payOrder(orderList)
    elif chosenOption == 'c':
        viewCart(orderList)
    elif chosenOption == 'h':
        viewOrderHistory(orderHistory)
    elif chosenOption == 'q':
        quit()

def quit():
    if orderList == []:
        print("Goodbye.")
        accountJSON.close()
        menuJSON.close()
        exit()
    
    userChoice = ""
    
    while userChoice != 'y' or userChoice != 'n':
        print("Your current orders will be discarded. Do you want to quit? (Y/N): ")
        userChoice = input().lower()
        
        if userChoice == 'y':
            clear()
            print("Thank you for ordering from our restaurant.")
            accountJSON.close()
            menuJSON.close()
            exit()
        elif userChoice == 'n':
            menu()
        
        print("Invalid choice. Please input either 'y' or 'n'.")
    

# this loads the external database, simulated by a json file.
accountJSON = open('accounts.json', 'r')
accountDatabase = json.load(accountJSON)

accountMatched = False

clear()

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
            clear()
            print("Welcome, " + username)
            orderHistory = currentAccount['orderHistory']
            accountMatched = True
            break

    clear()
    print("You have entered either an incorrect username or password. Please try again.")

menu()