import console
from os.path import exists

print("Reading words...")
currentWord = ""
incorrectGuesses = []
guessedLetters = []
words = []
appostrophes = False
while True:
    ia = input("Include appostrophes? (y/n) ")
    if ia == "y":
        appostrophes = True
        break
    elif ia == "n":
        break
cacheFile = "./.words-cache"
if appostrophes:
    cacheFile = "./.words-cache-apos"

if exists(cacheFile):
    print("Loading words from cache...")
    with open(cacheFile, 'r') as f:
        for line in f:
            words.append(line.strip().lower())
else:
    print("No cache found, generating... (this may take a while)")
    with open('./words.txt') as file:
        for line in file:
            w = line.strip().lower()
            if (not appostrophes and "'" in w) or (w in words):
                continue
            words.append(w)
    print("Saving words to cache...")
    with open(cacheFile, 'w') as f:
        for word in words:
            f.write(word + "\n")
print("Done reading words.")
wordlen = int(input("How long is your word? "))
for i in range(wordlen):
    currentWord += " "
print("Finding words of length", wordlen)
c = 0
for i in range(len(words)):
    if len(words[i-c]) != wordlen:
        words.pop(i-c)
        c += 1


def filterWords(cword):
    global words
    c = 0
    for i in range(len(words)):
        for j in range(len(cword)):
            if cword[j] == " ":
                if words[i-c][j] in guessedLetters:
                    # print(f"Removing {words[i-c][j]} from {words[i-c]}")
                    words.pop(i-c)
                    c += 1
                    break
                else:
                    continue
            if cword[j] != words[i-c][j]:
                words.pop(i-c)
                c += 1
                break


numGuesses = 0
while True:
    if len(words) == 0:
        print("No words left!")
        break
    elif len(words) == 1:
        currentWord = words[0]
        console.displayBoard(currentWord, incorrectGuesses, len(words))
        print(f"Number of Guesses: {numGuesses}")
        break
    totalLetterCount = len(words)
    letterCount = {}
    console.displayBoard(currentWord, incorrectGuesses, len(words))
    for word in words:
        wletters = []
        for letter in word:
            if letter in guessedLetters:
                continue
            if letter in letterCount:
                if letter not in wletters:
                    letterCount[letter] += 1
                    wletters.append(letter)
                    # print(f"lc[{letter}]: {letterCount[letter]}")
                else:
                    continue
            else:
                letterCount[letter] = 1
                wletters.append(letter)

        # print(f"{word}: {wletters}")

    sortedList = sorted(letterCount.items(), key=lambda x: x[1], reverse=True)

    def printSorted(list, start, count):
        for i in range(start, start+count):
            if i >= len(list):
                return
            print(f"{list[i][0]}: {list[i][1] / totalLetterCount * 100}%")

    def printWithMode(mode, start, count):
        if mode == "letter":
            printSorted(sortedList, start, count)
        elif mode == "word":
            for i in range(start, start+count):
                if i >= len(words):
                    return
                print(f"{i}: {words[i]}")

    c = 10
    l = ""
    mode = "letter"
    print(f"Mode: {mode}")
    printSorted(sortedList, 0, 10)
    while (not l.isalpha() or l in guessedLetters):
        l = input()
        if l == "":
            printWithMode(mode, c, 10)
            c += 10
        elif l == "?":
            console.displayBoard(currentWord, incorrectGuesses, len(words))
            c = 0
            mode = "word" if mode == "letter" else "letter"
            print(f"Mode: {mode}")
            printWithMode(mode, c, 10)
            c += 10
        elif l in guessedLetters:
            print("You already guessed that letter.")
            continue
    isCorrect = False
    guessedLetters.append(l)
    numGuesses += 1
    while True:
        answer = input("Was it correct? (y/n): ")
        if answer == "y":
            isCorrect = True
            break
        elif answer == "n":
            break
    if isCorrect:
        locations = input(
            f"Enter location(s) where {l} occurs starting with 1: ").split(',')
        for i in range(len(locations)):
            locations[i] = int(locations[i]) - 1
        for place in locations:
            if place >= len(currentWord) or place < 0:
                continue
            currentWord = currentWord[:place] + l + currentWord[place+1:]
            print(currentWord)
        filterWords(currentWord)
    else:
        incorrectGuesses.append(l)
        filterWords(currentWord)
