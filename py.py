import json
from os import system

orderList = ['Medium (12 inch)', 'BBQ Chicken', 'Pan Pizza', 'Cheese stuffed crust', ]

print(orderList)

def payOrder(orderList):
    menuDatabase = json.load(open('menu.json', 'r'))
    
    totalPrice = 0

    for x in orderList:
        totalPrice += menuDatabase[x][1]

    return totalPrice

print(payOrder(orderList))