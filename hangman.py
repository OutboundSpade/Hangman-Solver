def printHangman(num):
    if num == 0:
        print("""
 +---+
 |   |
     |
     |
     |
     |
=========
		""")
    elif num == 1:
        print("""
 +---+
 |   |
 O   |
     |
     |
     |
 =========
		""")
    elif num == 2:
        print("""
 +---+
 |   |
 O   |
 |   |
     |
     |
=========
		""")
    elif num == 3:
        print("""
 +---+
 |   |
 O   |
/|   |
     |
     |
=========
		""")
    elif num == 4:
        print("""
 +---+
 |   |
 O   |
/|\  |
     |
     |
=========
		""")
    elif num == 5:
        print("""
 +---+
 |   |
 O   |
/|\  |
/    |
     |
=========
		""")
    elif num == 6:
        print("""
 +---+
 |   |
 O   |
/|\  |
/ \  |
     |
=========
		""")
    else:
        print("""
 +---+
 |   |
 O   |
/|\  |
/ \  |
 X   |
=========
		""")