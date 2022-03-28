import gui
from md5 import MD5
from util import *
import secrets
import string

# anoooother commit 
alphabet = string.ascii_letters
## two 512-bit messages: one should be fixed, one should be changed
# # M1 will be a random message of 512 random bits. Use secrets to generate the random bits.
M1 = "".join(secrets.choice(alphabet) for i in range(16))
M2 = "We like turtles!"

if __name__ == "__main__":
    gui.start_app()


def write_to_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)
        f.close()


def start_cracking():

    generateQs()


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


def generateQs():

    bitconditions = {
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

    Q = {
        -3: "0011011000110111001101000011010100110010001100110011000000110001",
        -2: "0100010101000110010000110100010001000001010000100011100000111001",
        -1: "0011100100111000010000100100000101000100010000110100011001000101",
        0: "0011000100110000001100110011001000110101001101000011011100110110",
    }

    # for i in range(64):
    #     for t in range (3,17):
    #         if i == '.':
    #             Q[t].join('0')
    #         elif i == '0':
    #             Q[t].join('0')
    #         elif i == '1':
    #             Q[t].join('1')
    #         elif i == '^':
    #             Q[t].join(Q)

    for t in range(3, 17):
        for i in bitconditions[t]:
            if i == ".":
                Q[t].join("0")
            elif i == "0":
                Q[t].join("0")
            elif i == "1":
                Q[t].join("1")
            elif i == "^":
                Q[t].join(Q)
