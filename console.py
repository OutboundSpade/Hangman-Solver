import os
import hangman


def displayBoard(word, incorrectLetters, numofwords):
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')
    showIncorrect(incorrectLetters)
    hangman.printHangman(len(incorrectLetters))
    showWord(word)
    print()
    print(f"Possible words: {numofwords}")


def showIncorrect(incorrectLetters):
    print("Incorrect letters: ", end="")
    for letter in incorrectLetters:
        print(letter, end=" ")
    print("\n")


def showWord(word):
    for letter in word:
        if letter == " ":
            letter = "_"
        print("", letter, end=" ")
    print("\n")


def progressBar(num, total, length=20):
    bar = "["
    for i in range(num):
        if i < num-1:
            bar += "="
        else:
            bar += ">"
    for i in range(total - num):
        bar += " "
    bar += "] "
    return bar
