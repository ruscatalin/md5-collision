
import random
from re import M, S, U


# # generate a 32 bit word with random bits
# word = [random.getrandbits(1) for _ in range(16)]

def bsdr_naf(word):
    """
    Returns the binary signed digit representation non-adjacent form of a byte word (32 bits).
    The return value is a list of signed integers. (-1, 0, 1)
    """
    X = word
    Y = [bit for bit in reversed(X)]
    Y.pop()
    Y.insert(0, 0)

    return [(X[i] + Y[i]) % 2 - Y[i] for i in range(len(X))]

def get_bitconditions(hash1, hash2, index, t):
    """
    
    t is the index of the buffer in an array of 64 buffers.
    """
    i = index
    Q = hash1._get_Q()
    Q_prime = hash2._get_Q()

    # RL will rotate x with n bits to the left.
    RL = lambda x, n: (x << n) | (x >> (32 - n))
    # RR will rotate x with n bits to the right.
    RR = lambda x, n: (x >> n) | (x << (32 - n))

    dot     = (Q[t][i] == Q_prime[t][i])
    plus    = (Q[t][i] == 0 and Q_prime[t][i] == 1)
    minus   = (Q[t][i] == 1 and Q_prime[t][i] == 0)
    zero    = (Q[t][i] == 0 and Q_prime[t][i] == 0)
    one     = (Q[t][i] == 1 and Q_prime[t][i] == 1)
    hat     = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t-1][i])
    v       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t+1][i])
    exclmark= (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t-1][i])
    y       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t+1][i])
    m       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t-2][i])
    w       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t+2][i])
    hashtag = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t-2][i])
    h       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t+2][i]) 
    quesmark= (Q[t][i] == Q_prime[t][i] and (Q[t][i] == 1 or Q[t-2][i] == 0))
    q       = (Q[t][i] == Q_prime[t][i] and (Q[t+2][i] == 1 or Q[t][i] == 0))
    r       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RL(Q[t-1][i], 30))
    u       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RR(Q[t+1][i], 30))
    R       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RL(Q[t-1][i], 30))
    U       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RR(Q[t+1][i], 30))
    s       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RL(Q[t-2][i], 30))
    c       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RR(Q[t+2][i], 30))
    S       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RL(Q[t-2][i], 30))
    C       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RR(Q[t+2][i], 30))

    return {
        'dot': dot,
        'plus': plus,
        'minus': minus,
        'zero': zero,
        'one': one,
        'hat': hat,
        'v': v,
        'exclmark': exclmark,
        'y': y,
        'm': m,
        'w': w,
        'hashtag': hashtag,
        'h': h,
        'quesmark': quesmark,
        'q': q,
        'r': r,
        'u': u,
        'R': R,
        'U': U,
        's': s,
        'c': c,
        'S': S,
        'C': C
    }

# Constants taken from Table A-1, pg 193 in the thesis.
AC = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
RC = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
W = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2, 0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

def get_AC():
    return AC

def get_RC():
    return RC

def get_W():
    return W

# from pg 20 in the thesis
def get_RC(t):
    # returns [RCt, RCt+1, RCt+2, RCt+3]
    if t == 0 or t == 4 or t == 8 or t == 12:
        return [7, 12, 17, 22]
    elif t == 16 or t == 20 or t == 24 or t == 28:
        return [5, 9, 14, 20]
    elif t == 32 or t == 36 or t == 40 or t == 44:
        return [4, 11, 16, 23]
    elif t == 48 or t == 52 or t == 56 or t == 60:
        return [6, 10, 15, 21]


def get_differences(hash, hash_prime):
    Q = hash.get_Q()
    Q_prime = hash_prime.get_Q()
    F = hash.get_F()
    F_prime = hash_prime.get_F()
    T = hash.get_T()
    T_prime = hash_prime.get_T()
    w = 0 # TODO: Figure this out
    w_prime = 0 # TODO: Figure this out
    differences = []
    for t in range(0, 64):
        rc = get_RC(t)

        delta_Q = []
        for i in range(len(Q[t])):
            delta_Q.append((Q_prime[t][i] - Q[t][i]) % 2)

        
        delta_Q = bsdr_naf(delta_Q)
        
        delta_F = F_prime[t] - F[t]
        delta_w = 0 # TODO: Figure this out
        delta_T = T_prime[t] - T[t]

        differences.append({'Q': delta_Q, 'F': delta_F, 'w': delta_w, 'T': delta_T, 'RC': rc})

    return differences

def check_differences(d, dq, df, dw, dt, rc):
    if d['Q'] != d or d['F'] != df or d['w'] != dw or d['T'] != dt or d['RC'] != rc:
        return False
    return True


# Generate a list of values -1 to 1, where items with indices in positive are 1, and in negative are -1
# 1 => bit at pos x has to match, -1 => bit at pos x has to be different, 
def diff_list(positive = [], negative = []):
    lst = [0] * 32
    for pos in positive: 
        lst[pos] = 1
    for neg in negative:
        lst[neg] = -1
    return lst

# Table 2-3, pg 27 in the thesis.
def wang_first_path(hash, hash_prime):
    diff = get_differences(hash, hash_prime)
    for t in range(64):
        d = diff[t]
        rc = get_RC(t)
        
        if t <= 3:
            #Example for 0 <= t <= 3:
            #dQt = 0, dFt = 0, dwt = 0, dT=0, RCt = get_RC(t)
            expected_delta_Q = diff_list()
            correct = check_differences(d, expected_delta_Q, 0, 0, 0, rc)
            if not correct:
                return (False, t)
                
        elif t == 4:
            expected_delta_Q = diff_list()
            correct = check_differences(d, expected_delta_Q, 0, 2**31, 2**31, rc)
        
        elif t == 5:
            q_diffs = diff_list(range(6, 22), [22])
        elif t == 6: 
        elif t == 7: 
        elif t == 8:
        elif t == 9:
        elif t == 10:
        elif t == 11:
        elif t == 12:
        elif t == 13:
        elif t == 14:
        elif t == 15:
        elif t == 16:
        elif t == 17:
        elif t == 18:
        elif t == 19:
        elif t == 20:
        elif t == 21:
        elif t == 22:
        elif t == 23:
        elif t == 24:
        elif t == 25:
        elif t >= 26 and t <= 33:
        elif t == 34:
        elif t == 35:
        elif t == 36:
        elif t == 37:
        elif t >= 38 and t <= 49:
        elif t == 50:
        elif t >= 51 and t <= 59:
        elif t == 60:
        elif t == 61:
        elif t == 62:
        elif t == 63:
        elif t == 64:

    return (True, -1)




