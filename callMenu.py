import json
import time
from os import system, name

menuJSON = open('menu.json', 'r')
menuDatabase = json.load(menuJSON)
stuffing = menuDatabase['stuffing']

print(str(stuffing[0][0]))