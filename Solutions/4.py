from ChallengeClient import challengeinterface

#############################################################
# Function declarations
#############################################################
#rot-n function
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
# this is a different line in some levels, so pay attention
def select_rline(fulltext, rline):
    lines = fulltext.rsplit("\n")
    problemtext = lines[len(lines) - rline]
    return problemtext

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
        for n in range(1, 27):
            newword = rot_n(n, w)
            if newword in realwords:
                answer.append(newword)
                break

    # make answer into a string
    return ' '.join(answer)


#############################################################
# Main code starts here
if __name__ == "__main__":
    level = '4'
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

    # read in real word file and make it a list
    with open('wordlist.txt') as f:
        realwords = f.read().splitlines()

    # we have to answer 50 different questions :o
    correct = 0
    while (correct < 50):
        # solve the problem
        solution = solve_problem(problemtext, realwords)
        print('\nYour solution is:\n', solution)

        # submit the answer
        # If it's correct you get a flag
        # if it's incorrect you get a new challenge
        result = challenge.submit_answer(solution)
        print('\n Result is:\n', result)

        lines = result.rsplit("\n")
        if (lines[0] == "Correct!" or lines[0].startswith("Here is your flag")):
            correct += 1
        problemtext = select_rline(result, 2)

    # close the socket at the end of the program
    challenge.exit()