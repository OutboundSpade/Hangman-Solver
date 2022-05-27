import os

if os.name == 'posix':
    _ = os.system('clear')
else:
    _ = os.system('cls')

s = input("Search: ")
f = open("words.txt", "r")
for line in f:
    if s.lower() in line.lower():
        print(line.lower(), end="")
