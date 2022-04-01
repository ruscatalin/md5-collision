
import secrets
from wang import *

modular_add = lambda a, b: (a + b) % pow(2, 32)
modular_sub = lambda a, b: (a - b) % pow(2, 32)

# RL will rotate x with n bits to the left.
RL = lambda x, n: (x << n) | (x >> (32 - n))
# RR will rotate x with n bits to the right.
RR = lambda x, n: (x >> n) | (x << (32 - n))


# Constants taken from Table A-1, pg 193 in the thesis.
AC = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
RC = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
W = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2, 0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
IV_initial = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]


# Once we can validate the first 16 Qs, we can produce the corresponding message words, according to the formula from pg 25 of the thesis
# I think this reverses some MD5 steps, but I'm not sure
def generate_message_from_Qs(Q):

    def get_ft_16(Q_int, t):
        # From https://eprint.iacr.org/2004/264.pdf Table 3, pg 20
        # Apprently this how you calculate f[t] in the first 16 rounds
        # !!!! Should be equal to F[t]
        return (Q_int[t] & Q_int[t - 1]) ^ ((Q_int[t] ^ 0xFFFFFFFF) & Q_int[t - 2])

    Q_int = [int(Q[i], 2) for i in range(16)]

    message_words = [Q_int[0], Q_int[1], Q_int[2]]
    for t in range(3, 15):
        rr = RR(modular_sub(Q_int[t+1], Q_int[t]), RC[t])
        ft = get_ft_16(Q_int, t)
        word = modular_sub(rr, ft)
        word = modular_sub(word, Q_int[t-3])
        word = modular_sub(word, AC[t])
        message_words.append(word)
    return message_words


def get_differences(hash, hash_prime):
    Q = hash['Q']
    Q_prime = hash_prime['Q']
    T = hash['T']
    T_prime = hash_prime['T']
    F = hash['F']
    F_prime = hash_prime['F']
    m = hash['message']
    m_prime = hash_prime['message']


    def get_Q_differences(Q, Q_prime, t):
        delta_Q = []
        for i in range(len(Q[t])):
                if Q_prime[t][i] == 1 and Q[t][i] == 0:
                    delta_Q.append(1)
                elif Q_prime[t][i] == 0 and Q[t][i] == 1:
                    delta_Q.append(-1)
                else:
                    delta_Q.append(0)
        return delta_Q

    differences = []
    for t in range(64):
        
        delta_Q = []
        if t < 35:
            delta_Q = get_Q_differences(Q, Q_prime, t)
        else:
            delta_Q.append(modular_sub(Q_prime[t], Q[t]))

        if t >= 0:
            delta_F = modular_sub(F_prime[t], F[t])
            delta_T = modular_sub(T_prime[t], T[t])
            delta_w = modular_sub(m_prime[W[t]], m[W[t]])
            rc = RC[t]
        else:
            delta_F, delta_T, delta_w, rc = None, None, None, None 

        differences.append({'Q': delta_Q, 'F': delta_F, 'w': delta_w, 'T': delta_T, 'RC': rc})

    return differences  # This will have extra 3 elements at the beginning, according to the table 2-5

def check_differences(d, dq, df, dw, dt):
    if d['Q'] != dq or d['F'] != df or d['w'] != dw or d['T'] != dt:
        return False
    return True

# # Generate a list of values -1 to 1, where items with indices in positive are 1, and in negative are -1
# # 1 => bit at pos x has to match, -1 => bit at pos x has to be different, 
def generate_bsdr(positive = [], negative = []):
    lst = [0] * 32
    for pos in positive:
        lst[pos] = 1
    for neg in negative:
        lst[neg] = -1
    return lst


def int_list_to_concatenated_bytes(int_list):
    stringed = []
    for m in int_list:
        #convert m to bytes
        m_bytes = m.to_bytes(4, byteorder='big')
        stringed.append(m_bytes)

    concatenated_bytes = b''.join(stringed)
    return concatenated_bytes


def generate_valid_bytes(second_block=False, first_block_Qs=None):
    if not second_block:
        generated_Qs = generate_first16_Qs()
    else:
        generated_Qs = generate_first16_Qs_second_block(first_block_Qs)
    message = generate_message_from_Qs(generated_Qs)
    concatenated_bytes = int_list_to_concatenated_bytes(message)
    return concatenated_bytes, message


def write_to_file(filename, text):
    with open(filename, 'a') as f:
        f.write(text)
        f.close()
    