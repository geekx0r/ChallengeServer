from ChallengeClient import challengeinterface
import base64

#############################################################
# Function declarations
#############################################################
C_UPPER = range(ord('A'),ord('Z')+1) #goddammed +1 is required: fucked me up for an hour >_<
C_LOWER = range(ord('a'),ord('z')+1)

#rot-n function
def rot_n(n, msg):
    decoded = ''
    for c in msg:
        rotted = ord(c) + n
        if ord(c) in C_UPPER:
            if rotted > ord('Z'):
                rotted = (rotted - ord('Z')) + ord('A') - 1
                decoded += chr(rotted)
            else:
                decoded += chr(rotted)
        elif ord(c) in C_LOWER:
            if rotted > ord('z'):
                rotted = (rotted - ord('z')) + ord('a') - 1
                decoded += chr(rotted)
            else:
                decoded += chr(rotted)
        else:
            decoded += c

    return decoded

def all_casings(s):
    if not s:
        yield ""
    else:
        first = s[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(s[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(s[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing

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
    # split string into fragments
    # 4 b64 characters represents 3 ascii characters
    i = 0
    frag = []
    while (i < len(problemtext)):
        frag.append(problemtext[i:i + 4])
        i += 4

    possible_rots = []
    for n in range(0, 26):
        possible_rots.append(n)

    found = {}
    for f in frag:
        perms = all_casings(f)
        #print("frag",f)
        breakout = False
        for p in perms:
            if (breakout):
                breakout = False
                break
            #print("frag",f,"perm",p)
            for n in possible_rots:
                new_r = rot_n(n, p) + "==="
                new_b = base64.b64decode(new_r)
                try:
                    new_s = new_b.decode('ascii')
                    good = True
                    for c in new_s:
                        if (not (ord(c) in C_UPPER or ord(c) == ord(" "))):
                            good = False
                            #print(c, ord(c), "is not a good char")
                            break
                        #else:
                            #print(c,ord(c),"is a good char")
                    if (good):
                        #print(p, n, "->", new_r, "=>", new_s)
                        if (n not in found):
                           found[n] = []
                        found[n].append(p)
                        #breakout = True
                        #break
                except UnicodeDecodeError:
                    #print("decode error",n,new_r)
                    continue

        #print(found)
        #possible_rots = [*found.keys()]
        #print(possible_rots)

    #find longest array in found, which will give us the rot
    maxlen = 0
    index = -1
    for i in found:
        if (len(found[i]) > maxlen):
            maxlen = len(found[i])
            index = i
    coded = rot_n(index, "".join(found[index]))
    coded2 = base64.b64decode(coded)
    answer = coded2.decode('ascii')
    return answer

#############################################################
# Main code starts here
if __name__ == "__main__":
    level = '6'
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

    # solve the problem
    solution = solve_problem(problemtext)
    print('\nYour solution is:\n' + solution)

    # submit the answer
    result = challenge.submit_answer(solution)
    print('\n Result is:\n' + result)

    # close the socket at the end of the program
    challenge.exit()