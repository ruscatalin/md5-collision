from telnetlib import NOP
import gui
from md5 import MD5
from util import *
import secrets
import string
 
alphabet = string.ascii_letters
## two 512-bit messages: one should be fixed, one should be changed
# # M1 will be a random message of 512 random bits. Use secrets to generate the random bits.
M1 = "".join(secrets.choice(alphabet) for i in range(16))
M2 = "We like turtles!"



def write_to_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)
        f.close()


def start_cracking():


    Q = {
        -3: "01100111010001010010001100000001",
        -2: "11101111110011011010101110001001",
        -1: "10011000101110101101110011111110",
        0: "00010000001100100101010001110110",
        1: "",
        2: "",
        3: "",
        4: "",
        5: "",
        6: "",
        7: "",
        8: "",
        9: "",
        10: "",
        11: "",
        12: "",
        13: "",
        14: "",
        15: "",
        16: "",
    }

    M0 = []

    generateQs(Q)
    print(Q)
    deriveM0s(Q)

    M1 = M0 + [0, 0, 0, 0, 2^31, 0, 0, 0, 0, 0, 0, 2^15, 0, 0, 2^31, 0]



"""     global M1, M2

    hM1 = MD5.hash(M1)
    Q_M1 = MD5._get_Q()    
    hM2 = MD5.hash(M2)
    Q_M2 = MD5._get_Q()

    print("Started cracking...")

    while True:
        # Check the first 16 bitconditions of M1
        if wang_first_16_bitconditions(Q_M1):
            # Write M1 to a log file
            write_to_file('log.txt', '\n 3-16: ' + M1)
            if bitconditions16to64(Q_M1): # Check the remaining bitconditions of block1
                write_to_file('log.txt', '\n 16-64: ' + M1)
                break
        else: # Brute force, god speed
            M1 = ''.join(secrets.choice(alphabet) for i in range(16))
            hM1 = MD5.hash(M1)
            Q_M1 = MD5._get_Q()
    
    gui.update_output('Collision found: {}'.format(M1))
    gui.button_switch() """


def generateQs(Q):

    bitconditions = {
        1: "................................",
        2: "................................",
        3: "............0.......0....0......",
        4: "1.......0^^^1^^^^^^^1^^^^0......",
        5: "1...1.0.01..000000000000001..1.1",
        6: "0000001^01111111101111000100^0^1",
        7: "00000011111111101111100000100000",
        8: "000000011..100010.0.010101000000",
        9: "11111011...100000.1^111100111101",
        10: "01......0..111111101...001....00",
        11: "00..........00011100...011....10",
        12: "00....^^....10000001...10.......",
        13: "01....01....1111111....00...1...",
        14: "0.0...00....1011111....11...1...",
        15: "0.1...01........1...........0...",
        16: "0.1.............................",
    }

    

    for t in range(1, 17):
        for i in range (32):
            if bitconditions[t][i] == ".":
                Q[t] += "0"
            elif bitconditions[t][i] == "0":
                Q[t] += "0"
            elif bitconditions[t][i] == "1":
                Q[t] += "1"
            elif bitconditions[t][i] == "^":
                Q[t] += Q[t - 1][i]
        
        # print("Q -> ", Q[t])


# Python3 program for Left
# Rotation and Right
# Rotation of a String

# In-place rotates s towards left by d
def leftrotate(s, d):
	tmp = s[d : ] + s[0 : d]
	return tmp

# In-place rotates s
# towards right by d
def rightrotate(s, d):

    return leftrotate(s, len(s) - d)

# Driver code
if __name__=="__main__":
	
	str1 = "GeeksforGeeks"
	print(leftrotate(str1, 2))

	str2 = "GeeksforGeeks"
	print(rightrotate(str2, 2))

# This code is contributed by Rutvik_56


def ft_first16(x, y, z):
    return (x & y) ^ (~x ^ z) 

def deriveM0s(Q):
    # mt = RR(Qt+1 − Qt,RCt) − ft(Qt,Qt−1,Qt−2) − Qt−3 − ACt for 0 ≤ t ≤ 15.

    M0 = []

    for t in range (3):
        # print(int("0b" + Q[t + 1], 2) - int("0b" + Q[t], 2))
        print("0b" + Q[t + 1])
        print(rightrotate(Q[t+1] - Q[t], RC[t]))
        M0[t] = rightrotate(Q[t+1] - Q[t], RC[t]) - ft_first16(Q[t],Q[t-1],Q[t-2]) - Q[t-3] - AC[t] 

if __name__ == "__main__":
    # gui.start_app()
    start_cracking()