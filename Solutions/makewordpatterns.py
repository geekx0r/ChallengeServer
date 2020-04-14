# Makes the wordPatterns.py File
# http://inventwithpython.com/hacking (BSD Licensed)

# Creates wordpatterns.py based on the words in our dictionary
# text file, wordlist.txt.

import pprint

# Returns the word pattern for a given word, eg. "PUPPY" => "0.1.0.0.2"
def word_pattern(word):
    word = word.upper()
    next = 0
    letternums = {}
    wordpattern = []
    for letter in word:
        if letter not in letternums:
            letternums[letter] = str(next)
            next += 1
        wordpattern.append(letternums[letter])
    return '.'.join(wordpattern)

def main():
    allPatterns = {}

    fo = open('wordlist.txt')
    wordList = fo.read().splitlines()
    fo.close()

    for word in wordList:
        # Get the pattern for each string in wordList.
        pattern = word_pattern(word)

        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)

    # This is code that writes code. The 7-wordpatterns.py file contains
    # one very, very large assignment statement.
    fo = open('wordpatterns.py', 'w')
    fo.write('wpatterns = ')
    fo.write(pprint.pformat(allPatterns))
    fo.close()