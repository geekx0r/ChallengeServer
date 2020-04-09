from ChallengeClient import challengeinterface

#############################################################
# Function declarations
#############################################################

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
def solve_problem(problemtext):
    return problemtext


#############################################################
# Main code starts here
if __name__ == "__main__":
    level = '3'
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

    for i in range(0,50):
        #solve the problem
        solution=solve_problem(problemtext)
        print('\nYour solution is:\n',solution)

        #submit the answer
        result = challenge.submit_answer(solution)
        print('\n Result is:\n' + result)

        problemtext = select_rline(result, 2)

    # close the socket at the end of the program
    challenge.exit()