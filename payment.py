import json
from os import system
system('cls')

with open('menu.json', 'r') as menuJSON:
    menuDatabase = json.load(menuJSON)
    codes = menuDatabase["codes"]
    
# we generally display orders in the same way throughout the system, so this function reduces repetition.
def printFormattedOrder(orderList):
    # this will count down from the length of the list
    # to assign each element an order number.
    orderNumber = len(orderList)

    for order in reversed(orderList):
        orderNumber -= 1
        
        # print a number that represents the order number. then, print each individual element of the order 
        print("(", orderNumber, ") ( x", order[4], ")")
        for count, part in enumerate(order[:4]):
            if count == 4:
                print("\n")
            print("     ", part)
        print("     ", order[6])
        print("     ", "Php", "{0:.2f}".format(order[5]))
    return

def addDiscount(orderList):
    while True:
        printFormattedOrder(orderList)
        discountMethod = str(input("Enter 'I' for a PWD ID discount, 'C' for a discount code, 'S' for senior citizen, or 'ND' for no discount: ").lower())
        
        if discountMethod == "i" or discountMethod == "c" or discountMethod == "s" or discountMethod == "nd":
            
            if discountMethod == "i":
                system('cls')
                print("PWD discount selected.")

                discount = 0.9
                print(f"%{round((1-discount)*100, 1)} OFF")

            elif discountMethod == "c":
                system('cls')
                print("Discount code selected.")

                while True:
                    icode = str(input("Type your discount code here: "))
                    system('cls')
                    leave = 'n'
                    keyFound = False
                    for key, value in codes.items(): #this searches the list for the codes
                        if icode == key:
                            print("valid code") 

                            discount = value
                            print(f"%{round((1-discount)*100, 1)} OFF")
                            keyFound = True
                            break
                    
                    if not keyFound: #if by the end of the list there are no matching codes, then
                        print("CODE IS INVALID or EXPIRED")
                        while True:
                            leave = str(input("Enter another code? y/n?")).lower()

                            if leave == 'y':
                                system('cls')
                                break
                            elif leave == 'n':
                                system('cls')
                                discount = 1
                                print("NO DISCOUNT ADDED")
                                print(f"%{round((1-discount)*100, 1)} OFF")

                                break
                            else:
                                system('cls')
                                print("Enter only 'y' or 'n'")
                    if leave == 'y':
                        continue
                    else:
                        break
                    
            elif discountMethod == "s":
                system('cls')
                print("Senior citizen discount selected.")

                discount = 0.7
                print(f"%{round((1-discount)*100, 1)} OFF")

            elif discountMethod == "nd":
                discount = 1
                print("NO DISCOUNT ADDED")
                print(f"%{round((1-discount)*100, 1)} OFF")

            break
        else:
            print("INVALID INPUT")

    return discount


def payOrder(orderList, openedAccount):
    totalPrice = 0
    paymentSuccessful = False
    
    if orderList == []:
        print("Current order is empty. Press ENTER to return to the main menu.")
        input()
        return paymentSuccessful
    
    # calculate total price across all orders.
    for order in orderList:
        totalPrice += order[-2]
    
    print("----------------------------------------------")
    print(str("Total Price: {0:.2f}".format(totalPrice)))
    

    while True:
        printFormattedOrder(orderList)
        paymentPath = input("To add a discount, enter 'D'. To proceed with payment, enter 'P'. To cancel, type 'C'. ").lower()
    
        system('cls')

        if paymentPath == "d":
            system('cls')
            originalPrice = totalPrice
            totalPrice = totalPrice * addDiscount(orderList)
            print("----------------------------------------------")
            print(str("Total Price: {0:.2f}".format(originalPrice)))
            print(str("Total Price With Discount: {0:.2f}".format(totalPrice)))

            while True:
                print("----------------------------------------------")
                print(str("Amount to Pay: {0:.2f}".format(totalPrice)))
                
                cash = None
                
                while cash == None:
                    try: 
                        cash = float(input("Enter Cash Amount: "))
                    except:
                        print("Please enter a numerical value.")
                
                if type(cash) == str:
                    system('cls')
                    print("ENTER ONLY NUMERICAL VALUES")

                elif cash == totalPrice:
                    system('cls')
                    print("----------------------------------------------")
                    print("Exact Amount Given")
                    break

                elif cash > totalPrice:
                    system('cls')
                    change = cash - totalPrice
                    print("----------------------------------------------")
                    print(str("Amount to Return: {0:.2f}".format(change)))
                    break
                else:
                    system('cls')
                    print("Insufficent Amount Given")

            break
        
        elif paymentPath == "p":

            while True:
                system('cls')
                print("----------------------------------------------")
                print(str("Total Price With Discount: {0:.2f}".format(totalPrice)))
                
                cash = None
                
                while cash == None:
                    try:
                        cash = float(input("Enter Cash Amount: "))
                    except:
                        print("Please enter a numerical value.")
                
                if cash == totalPrice:
                    system('cls')
                    print("----------------------------------------------")
                    print("Exact Amount Given")
                    break

                elif cash > totalPrice:
                    system('cls')
                    change = cash - totalPrice
                    print("----------------------------------------------")
                    print(str("Amount to Return: {0:.2f}".format(change)))
                    break
                else:
                    system('cls')
                    print("Insufficent Amount Given")
            break

        elif paymentPath == "c":
            return paymentSuccessful
        else:
             print("----------------------------------------------")
             print("INVALID INPUT")
             print(str("Total Price: {0:.2f}".format(totalPrice)))
    with open('accounts.json', mode = 'r') as accountsJSONIn:
        accountData = json.load(accountsJSONIn)
        for order in orderList:
            currentHistory = accountData[openedAccount]["orderHistory"].append(order)

    with open('accounts.json', mode = 'w') as menuJSONOut:
        menuJSONOut.write(json.dumps(accountData, indent = 4))
        paymentSuccessful = True
        
    print("Payment successful. Press ENTER to go back to the main menu.")
    input()
    return paymentSuccessful