from ChallengeClient import challengeinterface
import os, re, copy, makewordpatterns

#############################################################
# Initiation
#############################################################
#read in real word file and make it a list
f = open('WordList.txt')
realwords = set(f.read().splitlines())
f.close()

#make and import word patterns dict
if not os.path.exists('wordpatterns.py'):
    makewordpatterns.main()  # create the wordpatterns.py file
import wordpatterns as wp  # we now have a dictionary called wp.wpatterns that we can use

#Constants
C_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
C_FLAG = 'Here is your flag ->'

#############################################################
# Function declarations
#############################################################
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

# Returns a dictionary value that is a blank cipherletter mapping.
def getBlankCipherletterMapping():
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}

# The letterMapping parameter is a "cipherletter mapping" dictionary
# value that the return value of this function starts as a copy of.
# The cipherword parameter is a string value of the ciphertext word.
# The candidate parameter is a possible English word that the
# cipherword could decrypt to.

# This function adds the letters of the candidate as potential
# decryption letters for the cipherletters in the cipherletter
# mapping.
def addLettersToMapping(letterMapping, cipherword, candidate, onlyadd=False):
    letterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            if (not onlyadd or len(letterMapping[cipherword[i]]) == 0):
                letterMapping[cipherword[i]].append(candidate[i])
    return letterMapping

# To intersect two maps, create a blank map, and then add only the
# potential decryption letters if they exist in BOTH maps.
def intersectMappings(mapA, mapB):
    intersectedMapping = getBlankCipherletterMapping()
    for letter in C_LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping

# Cipher letters in the mapping that map to only one letter are
# "solved" and can be removed from the other letters.
# For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
# maps to ['N'], then we know that 'B' must map to 'N', so we can
# remove 'N' from the list of what 'A' could map to. So 'A' then maps
# to ['M']. Note that now that 'A' maps to only one letter, we can
# remove 'M' from the list of letters for every other
# letter. (This is why there is a loop that keeps reducing the map.)
def removeSolvedLettersFromMapping(letterMapping):
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # solvedLetters will be a list of uppercase letters that have one
        # and only one possible mapping in letterMapping
        solvedLetters = []
        for cipherletter in C_LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # If a letter is solved, than it cannot possibly be a potential
        # decryption letter for a different ciphertext letter, so we
        # should remove it from those other lists.
        for cipherletter in C_LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again.
                        loopAgain = True
    return letterMapping


def decryptWithCipherletterMapping(ciphertext, letterMapping):
    translated = ""
    for symbol in ciphertext:
        if (len(letterMapping[symbol]) == 1):
            translated += letterMapping[symbol][0]
        else:
            translated += "."
    return translated

def match(input_string, string_list):
    pattern = re.compile("^" + input_string + "$")
    ret = []
    for s in string_list:
        if (pattern.match(s)):
            ret.append(s)
    return ret

# select_rline
# Takes the full challenge text as input and trims it down to
# the line that you input, counting from the end of the string
# e.g. if you input line=2, it will return the second last line
def select_rline(fulltext, rline):
    lines = fulltext.rsplit("\n")
    problemtext = lines[len(lines) - rline]
    return problemtext

# solve_problem
# Solve the problem in this function
def solve_problem(problemtext):
    # split question data into a list of words
    codedwordlist = problemtext.split()

    intersectedMap = getBlankCipherletterMapping()

    # make new array of words in descending order by length
    codedwordlist_sorted = sorted(codedwordlist, reverse=True, key=len)

    # loop through words - only the longest 12
    for i in range(0, 12):
        w = codedwordlist_sorted[i]

        # Get a new cipherletter mapping for each ciphertext word.
        newMap = getBlankCipherletterMapping()

        p = word_pattern(w)

        if p not in wp.wpatterns:
            continue  # This word was not in our dictionary, so continue

        # Add the letters of each candidate to the mapping.
        for candidate in wp.wpatterns[p]:
            newMap = addLettersToMapping(newMap, w, candidate)

        # Intersect the new mapping with the existing intersected mapping.
        intersectedMap = intersectMappings(intersectedMap, newMap)

    # Remove any solved letters from the other lists.
    mapping = removeSolvedLettersFromMapping(intersectedMap)

    # use incomplete mapping and dictionary to guess remaining mappings
    for w in codedwordlist:
        for i in range(len(w)):
            if len(mapping[w[i]]) != 1:
                # Look up in dictionary
                reword = decryptWithCipherletterMapping(w, mapping)
                # print reword
                matchwords = match(reword, realwords)
                if (len(matchwords) == 1):
                    mapping[w[i]] = list(matchwords[0][i])

    decrypted = []
    for w in codedwordlist:
        decrypted.append(decryptWithCipherletterMapping(w, mapping))

    decrypted_str = ' '.join(decrypted)

    return decrypted_str

#############################################################
# Main code starts here
if __name__ == "__main__":
    level = '7'
    serverip = "15.223.13.29"
    challengeport = 8001

    # start the challenge game
    challenge = challengeinterface(serverip, challengeport)
    print(challenge.start())

    # choose the level to run
    challengetext = challenge.select_level(level)
    print('\nChallenge Text is:\n' + challengetext)

    # trim the text down to the problem statement
    problemtext = select_rline(challengetext, 2)
    print('Problem Text is:\n' + problemtext)

    won = False
    while (not won):
        # solve the problem
        solution = solve_problem(problemtext)
        print('\nYour solution is:\n' + solution)

        # submit the answer
        result = challenge.submit_answer(solution)
        print('\nResult is:\n' + result)

        if (C_FLAG in result):
            won = True
        else:
            problemtext = select_rline(result, 2)
            print('Problem Text is:\n' + problemtext)

    # close the socket at the end of the program
    challenge.exit()