import json
import time
import payment
from os import system, name

# orders in both orderList and orderHistory are arrays that are structured as follows:
# [0] Crust size,
# [1] Toppings,
# [2] Crust type,
# [3] Crust stuffing,
# [4] Quantity (integer),
# [5] Price (float),
# [6] Timestamp
# Example: ["Small - 10 inch", "Pepperoni", "Thin crust", "Cheese stuffed crust", 2, 469.00, "2023-03-26, 10:39:45"]
orderList = []
menuJSON = open('menu.json', 'r')
menuDatabase = json.load(menuJSON)
paymentSuccessful = False

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
        orderList.append([None, None, None, None, None, None, None])
        
        # set current order to the last one in the list (.append() adds an item to the end of a list)
        currentOrder = orderList[-1]
        
        # a two dimensional array containing 
        selectorOutput = [None, None, None, None, None]
    
    # number of dashes between the price/order ui on top and the menu
    dividerLength = 130
    
    # initialize the price with the base price as defined in the dictionary
    price = menuDatabase['basePrice']
    
    while page < 7:
        system('cls')
        currentTime = time.strftime('%Y-%m-%d, %I:%M:%S')
        
        # shows the user what their order is so far
        print("| Current pizza:", end = " ")
        for part in currentOrder[:4]:
            if part != None:
                print(part, end = " ")
        
        # prints first half of the second menu row
        print("|\n| Menu \t\t | Php " + "{0:.2f}".format(price), end = "\t\t")
        match page:
            # crust size
            case 0:
                print("| [1. Crust Size] - 2. Toppings - 3. Dough - 4. Stuffing - 5. Quantity - 6. Review Order |")
                print("-" * dividerLength)
                # selector() returns a list containing the selected item and the price.
                # Example: ["Small (10 inch)", 0.00]
                selectorOutput[page] = (selector(menuDatabase['sizes']))
            # toppings
            case 1:
                print("| 1. Crust Size - [2. Toppings] - 3. Dough - 4. Stuffing - 5. Quantity - 6. Review Order |")
                print("-" * dividerLength)
                selectorOutput[page] = (selector(menuDatabase['toppings']))
            # dough
            case 2:
                print("| 1. Crust Size - 2. Toppings - [3. Dough] - 4. Stuffing - 5. Quantity - 6. Review Order |")
                print("-" * dividerLength)
                selectorOutput[page] = (selector(menuDatabase['dough']))
            # stuffing
            case 3:
                print("| 1. Crust Size - 2. Toppings - 3. Dough - [4. Stuffing] - 5. Quantity - 6. Review Order |")
                print("-" * dividerLength)
                selectorOutput[page] = (selector(menuDatabase['stuffing']))
            # quantity
            case 4:
                print("| 1. Crust Size - 2. Toppings - 3. Dough - 4. Stuffing - [5. Quantity] - 6. Review Order |")
                selectorOutput[page] = quantitySelector()            
            # review
            case 5:
                print("| 1. Crust Size - 2. Toppings - 3. Dough - 4. Stuffing - 5. Quantity - [6. Review Order] |")
                print("-" * dividerLength)
                currentOrder[page] = price
            # append timestamp to order
            case other:
                currentOrder[page] = currentTime
                return
        
        # calls the orderPageSeletor() function, which returns either a 1 or -1 based on if the user wants to go to the next or previous page.
        pageOperation = orderPageSelector(page)
        
        # quantity and review order page have different procedures
        if page < 4:
            # add the outputted item (like the toppings, dough, etc. to the appropriate part of the current order array).
            currentOrder[page] = selectorOutput[page][0]
            if pageOperation == 1:
                price += selectorOutput[page][1]
            else:
                price -= selectorOutput[page - 1][1]
        elif page == 4:
            currentOrder[page] = selectorOutput[page]
            
            if pageOperation == 1:
                price *= selectorOutput[page]
            else:
                price -= selectorOutput[page - 1][1]
        elif page == 5:
            if pageOperation == -1:
                price /= selectorOutput[page - 1]
        
        # add 1 or -1 to the current page based on user selection.
        page += pageOperation
    return orderList

# this function asks the cashier to provide the number of this order that the customer wants.
def quantitySelector():
    quantity = 0
    while quantity == 0:
        choice = input("Ask the customer how many of this pizza they want and input it here: ")
        try:
            int(choice)
        except:
            print("Please input a valid number.")
        
        if choice == 0:
                print("Please input a number greater than 0.")
        else:
            quantity = int(choice)
    return quantity

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
    # returns an array containing the name and price of the choice.
    # Example: ["Small (10 inch)", 0.00]
    return list[selectedChoice]

# orderPageSelector() return either 1 or -1 if the user wants to go to the next page or the previous one.
# we can add that to the current page value to change the page.
def orderPageSelector(page):
    selectedChoice = None
    if page == 0:
        return 1
    elif page == 5:
        while selectedChoice == None:
            choice = input("Verify with the customer that the pizza they have chosen so far is correct.\nWould you like to go back to the menu? (N to go back to the menu, P to go to the previous page): ").lower()
            if choice == 'n':
                return 1
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

def viewOrderHistory(orderHistory):
    if orderHistory == []:
        print("The order history is empty. Press ENTER to go back to the main menu.")
        input()
        return
    
    print("| Order History |")
    print("| This list is sorted from newest to oldest. |")
    print("----------------------------------------------")
    
    # .index() gets the first item that matches the given parameter,
    # meaning that duplicate items would break the system.
    payment.printFormattedOrder(orderHistory)
        
    input("Press ENTER to go back to the main menu.")
    return

def viewCart(orderList):
    if orderList == []:
        print("There are no items in the current order. Press ENTER to go back to the main menu.")
        input()
        return
    selectedChoice = None
    
    while selectedChoice == None:
        print("| View current order |")
        print("| This list is sorted from newest to oldest. |")
        print("----------------------------------------------")
        
        payment.printFormattedOrder(orderList)

        try:
            choice = input("Type the number of the order you would like to modify or press M to go back to the main menu: ")
            if choice == 'm' or choice == 'M':
                return
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
    print("| View your cart | You are editing order", selectedChoice, "|")
    
    # print a number that represents the order number. then, print each individual element of the order 
    print("(", selectedChoice, ") ( x", selectedOrder[4], ")")
    for part in selectedOrder[:4]:
        print("     ", part)
    print("     ", selectedOrder[6])
    print("     ", "Php", "{0:.2f}".format(selectedOrder[5]))

    
    choice = input("Press E to edit the order, D to delete it, or M to go back: ").lower()
    if choice == 'e':
        addOrder(selectedChoice)
    elif choice == 'd':
        orderList.pop(selectedChoice)
        clear()
        print("Order " + str(selectedChoice) + " removed.")
        viewCart(orderList)
    elif choice == 'm':
        clear()
        viewCart(orderList, selectedChoice)
    return

def menu(orderList, message = None):
    currentTime = time.strftime('%H:%M')
    currentDate = time.strftime('%A %B %d, %Y')
    
    chosenOption = None
    
    if message != None:
       print("|", str(message), " ")
       message = None
    
    while chosenOption != 'q':
        clear()
        
        print("|", currentTime, "|", currentDate, "|")
        print("| Type a letter corresponding to your desired menu option. |")
        print("| (T)ake customer order - (P)rint receipt - Modify (C)urrent Order - View order (h)istory - (Q)uit |")
        
        chosenOption = input().lower()
        clear()
    
        if chosenOption == 't':
            addOrder()
        elif chosenOption == 'p':
            paymentSuccessful = payment.payOrder(orderList, openedAccount)
            if paymentSuccessful:
                orderList.clear()
                paymentSuccessful = False
        elif chosenOption == 'c':
            viewCart(orderList)
        elif chosenOption == 'h':
            with open('accounts.json', mode = 'r') as accountsJSONIn:
                accountData = json.load(accountsJSONIn)
                orderHistory = accountData[openedAccount]["orderHistory"]
            viewOrderHistory(orderHistory)
        elif chosenOption == 'q':
            # if the user chooses not to quit when an order is still in progress, chosenOption will be reset to a blank state, allowing the loop to continue.
            chosenOption = quit()

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
            print("Goodbye.")
            accountJSON.close()
            menuJSON.close()
            exit()
        elif userChoice == 'n':
            return ""
        
        print("Invalid choice. Please input either 'y' or 'n'.")
    

# this loads the external database, simulated by a json file.
accountJSON = open('accounts.json', 'r')
accountDatabase = json.load(accountJSON)

accountMatched = False

clear()

# repeat the login process while a valid username and password have not been entered yet.
while not accountMatched:
    print("Pizza Ordering System")
    print("Please enter your username and password.")
    
    # prompts user for username and password.
    username = input("Username: ")
    password = input("Password: ")

    # checks input against database.
    for account in accountDatabase:
        currentAccount = accountDatabase[account]
        if username == currentAccount['username'] and password == currentAccount['password']:
            clear()
            orderHistory = currentAccount['orderHistory']
            accountMatched = True
            # save account number (not username) as opened account for modification of account history.
            openedAccount = account
            break

    clear()
    print("You have entered either an incorrect username or password. Please try again.")

menu(orderList, "Welcome, " + username + ".")