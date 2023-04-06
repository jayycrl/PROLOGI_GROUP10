import json
from os import system
system('cls')

menuJSON = open('menu.json', 'r')
menuDatabase = json.load(menuJSON)

orderList = [
["Small (10 inch)", "Pepperoni", "Thin crust", "Cheese stuffed crust", 1, 469.00, "2023-03-26, 10:39:45"], 
["Small (10 inch)", "Pepperoni", "Thin crust", "Cheese stuffed crust", 1, 469.00, "2023-03-26, 10:39:45"], 
["Small (10 inch)", "Pepperoni", "Thin crust", "Cheese stuffed crust", 1, 469.00, "2023-03-26, 10:39:45"],
]


codes = {
    '123456': 0.9,
    '121212': 0.8,
    '12345678': 0.7,
    'free99': 0,
}

def addDiscount():
    while True:
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
                    w = 0
                    leave = 'n'
                    for x in codes: #this searches the list for the codes
                        if icode == x:
                            print("valid code") 

                            discount = codes[x]
                            print(f"%{round((1-discount)*100, 1)} OFF")

                            break
                        else:
                            w += 1
                            if w == len(codes): #if by the end of the list there are no matching codes, then
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


def payOrder(orderList):    
    totalPrice = 0
    
    # calculate total price across all orders.
    for order in orderList:
        totalPrice += order[-2]
    
    print("----------------------------------------------")
    print(str("Total Price: {0:.2f}".format(totalPrice)))
    

    while True:
        paymentPath = input("To add a discount, enter 'D'. To proceed with payment, enter 'P'. To cancel, type 'C'. ").lower()
    
        system('cls')

        if paymentPath == "d":
            system('cls')
            originalPrice = totalPrice
            totalPrice = totalPrice * addDiscount()
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
            return

        else:
             print("----------------------------------------------")
             print("INVLAID INPUT")
             print(str("Total Price: {0:.2f}".format(totalPrice)))