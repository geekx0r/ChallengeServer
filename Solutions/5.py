from ChallengeClient import challengeinterface

#############################################################
# Function declarations
#############################################################
#read in real word file and make it a list
f = open('WordList.txt')
realwords = set(f.read().splitlines())
f.close()

#protocol constants (ie. responses we will get)
C_QUESTION_WORD_POST = "?"
C_RESPONSE_WRONG_PRE = "Incorrect! The answer was "
C_RESPONSE_CORRECT_PRE = "Correct!"
C_STARTOVER_PRE = "You have answered too many questions in a row wrong"
C_FLAG = "Here is your flag"

#rot-n function - only works for uppercase
def rot_n(n, msg):
    decoded = ''
    for char in list(msg):
            if char.isalpha():
                    value = ord(char) + n
                    if value > ord('Z'):
                            value = (value - ord('Z')) + ord('A') - 1
                    decoded += chr(value)
            else:
                    decoded += char
    return decoded

# select_rline
# Takes the full challenge text as input and trims it down to
# the line that you input, counting from the end of the string
# e.g. if you input line=2, it will return the second last line
def select_rline(fulltext, rline):
    lines = fulltext.rsplit("\n")
    problemtext = lines[len(lines) - rline][:-len(C_QUESTION_WORD_POST)]
    return problemtext

# select_answer
# Takes the full challenge text as input and trims it down to
# the right answer, when you got it wrong
def select_answer(fulltext):
    lines = fulltext.rsplit("\n")
    answertext = lines[0][len(C_RESPONSE_WRONG_PRE):]
    return answertext

# solve_problem
# Solve the problem in this function
def solve_problem(problemtext, realwords):
    # split question data into a list of words
    codedwordlist = problemtext.split()

    # set up variable for answer
    answer = []

    # loop through words
    for w in codedwordlist:
        # loop through rot-n functions until a match is found
        for n in range(0, 25):
            newword = rot_n(n, w)
            if newword in realwords:
                answer.append(newword)
                break

    # make answer into a string
    return ' '.join(answer)


#############################################################
# Main code starts here
if __name__ == "__main__":
    level = '5'
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
    print('\nProblem Text is:\n' + problemtext)

    won = False

    # make dict to keep track of answers
    answers = {}

    # the great loop
    while (not won):
        # choose the level to run
        result = challenge.select_level('5')
        print(result)

        while (True):
            q = select_rline(result, 2)

            if (q in answers):
                a = answers[q]
            else:
                a = "SPLINE"

            print('>>>SEND:  ', a)
            result = challenge.submit_answer(a)
            print(result)

            if (C_STARTOVER_PRE in result):
                break
            elif (C_FLAG in result):
                won = True
                break
            elif (C_RESPONSE_WRONG_PRE in result):
                # if it was wrong, store right answer
                answers[q] = select_answer(result)

    # close the socket at the end of the program
    challenge.exit()