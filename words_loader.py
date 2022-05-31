import os
import subprocess
import console
import sys

CACHE_VERSIONS = ["1.0.0"]

GENERATOR_FILE = "cache_generator"


def loadWords(cache_file, words_list, word_length, include_apos=False) -> list:
    """
    Load the words from the file into a list.
    """
    words = []

    if os.name == "nt":
        global GENERATOR_FILE
        GENERATOR_FILE += ".exe"
    if canReadFromCache(cache_file):
        print(f"Loading words from cache ...")
        print(f"Finding section with length {word_length} ...")
        words = loadFromCache(cache_file, word_length)
    else:
        print(f"No cache file found, generating new cache file ...")
        createCacheFile(GENERATOR_FILE, cache_file, include_apos, words_list)
        words = loadWords(cache_file, words_list, word_length, include_apos)
    return words


def createCacheFile(generator_file: str, cache_file: str, include_apos: bool, words_file: str) -> None:
    """
    Create the cache file.
    """
    generator_file = os.path.abspath(generator_file)
    if not os.access(generator_file, os.EX_OK):
        print(f"UNABLE TO RUN {generator_file}")
        exit(1)
    pArgs = [os.path.abspath(generator_file), "-file",
             words_file, "-out", cache_file]
    if not include_apos:
        pArgs.append("-ignore-apos")
    process = subprocess.Popen(
        pArgs, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    print(console.progressBar(0, 100))
    while process.poll() is None:
        out = process.stdout.readline().strip()
        if out != '':
            try:
                out = float(out)
            except ValueError:
                continue
            # print("\b"*200, end="")
            sys.stdout.write("\033[F")  # Cursor up one line
            print(console.progressBar(int(out), 100))
    process.wait()
    if process.returncode != 0 or not os.access(cache_file, os.R_OK):
        print(
            f"ERROR RUNNING {generator_file} ({process.returncode}): \n{out[1]}")
        exit(1)

    # with open(cache_file, 'w') as f:
    #     f.write()


def loadFromCache(cache_file, word_length) -> list:
    """
    Load the words from the cache file.
    """
    cFile = getSection(cache_file)
    if not canReadFromCache(cache_file):
        print("COULD NOT READ CACHE FILE! - in loadFromCache()")
        exit(1)
    meta = next(cFile)
    for line in meta:
        if line.startswith("WordCount: "):
            print(f"Found {line.split(': ')[1]} words in cache file.")
    for section in cFile:
        # print(f"Loading section {section[0]}")
        if section[0].isnumeric() and int(section[0]) == word_length:
            return next(cFile)
    print("COULD NOT FIND SECTION WITH LENGTH", word_length, "IN CACHE FILE!")
    exit(1)
    return


def getSection(cache_file) -> list:
    """
    Get the section of the cache file.
    """
    f = open(cache_file, 'r')
    line = f.readline().strip()
    while line != '':
        words = []
        while line != ';':
            if line != '':
                words.append(line)
            line = f.readline().strip()
        line = f.readline().strip()
        yield words
    f.close()


def canReadFromCache(cache_file) -> bool:
    """
    Check if the cache file exists and is readable.
    """
    # try:
    if not os.access(cache_file, os.R_OK):
        return False
    cFile = getSection(cache_file)
    section = next(cFile)
    for line in section:
        if line.startswith("Version: "):
            return line.split("Version: ")[1] in CACHE_VERSIONS
    print("CACHE FILE IS INVALID! (COULD NOT FIND VERSION)")
    exit(1)
    # return
    # with open(cache_file, 'r') as f:
    #     line = f.readline()
    #     while(line != ';'):
    #         if line.startswith('Version: '):
    #             print(line.split(': ')[1])
    #             if line.split(': ')[1] in CACHE_VERSIONS:
    #                 return True
    #             return False
    #     print("COULD NOT FIND VERSION IN CACHE FILE!")
    #     return False
    # except:
    #     return False
