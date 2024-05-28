import os

def clear():
   # for windows
   if os.name == 'nt':
       os.system('cls')
   else:
       os.system('clear')