
import random
from re import M, S, U


modular_add = lambda a, b: (a + b) % pow(2, 32)
modular_sub = lambda a, b: (a - b) % pow(2, 32)

# RL will rotate x with n bits to the left.
RL = lambda x, n: (x << n) | (x >> (32 - n))
# RR will rotate x with n bits to the right.
RR = lambda x, n: (x >> n) | (x << (32 - n))

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

# def get_bitconditions(hash1, hash2, index, t):
#     """
    
#     t is the index of the buffer in an array of 64 buffers.
#     """
#     i = index
#     Q = hash1._get_Q()
#     Q_prime = hash2._get_Q()


#     dot     = (Q[t][i] == Q_prime[t][i])
#     plus    = (Q[t][i] == 0 and Q_prime[t][i] == 1)
#     minus   = (Q[t][i] == 1 and Q_prime[t][i] == 0)
#     zero    = (Q[t][i] == 0 and Q_prime[t][i] == 0)
#     one     = (Q[t][i] == 1 and Q_prime[t][i] == 1)
#     hat     = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t-1][i])
#     v       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t+1][i])
#     exclmark= (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t-1][i])
#     y       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t+1][i])
#     m       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t-2][i])
#     w       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == Q[t+2][i])
#     hashtag = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t-2][i])
#     h       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - Q[t+2][i]) 
#     quesmark= (Q[t][i] == Q_prime[t][i] and (Q[t][i] == 1 or Q[t-2][i] == 0))
#     q       = (Q[t][i] == Q_prime[t][i] and (Q[t+2][i] == 1 or Q[t][i] == 0))
#     r       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RL(Q[t-1][i], 30))
#     u       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RR(Q[t+1][i], 30))
#     R       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RL(Q[t-1][i], 30))
#     U       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RR(Q[t+1][i], 30))
#     s       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RL(Q[t-2][i], 30))
#     c       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == RR(Q[t+2][i], 30))
#     S       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RL(Q[t-2][i], 30))
#     C       = (Q[t][i] == Q_prime[t][i] and Q[t][i] == - RR(Q[t+2][i], 30))

#     return {
#         'dot': dot,
#         'plus': plus,
#         'minus': minus,
#         'zero': zero,
#         'one': one,
#         'hat': hat,
#         'v': v,
#         'exclmark': exclmark,
#         'y': y,
#         'm': m,
#         'w': w,
#         'hashtag': hashtag,
#         'h': h,
#         'quesmark': quesmark,
#         'q': q,
#         'r': r,
#         'u': u,
#         'R': R,
#         'U': U,
#         's': s,
#         'c': c,
#         'S': S,
#         'C': C
#     }

# Constants taken from Table A-1, pg 193 in the thesis.
AC = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
RC = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
W = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2, 0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
IV_initial = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
def get_AC():
    return AC

def get_RC():
    return RC

def get_W():
    return W

# # from pg 20 in the thesis
# def get_RC(t):
#     # returns [RCt, RCt+1, RCt+2, RCt+3]
#     if t == 0 or t == 4 or t == 8 or t == 12:
#         return [7, 12, 17, 22]
#     elif t == 16 or t == 20 or t == 24 or t == 28:
#         return [5, 9, 14, 20]
#     elif t == 32 or t == 36 or t == 40 or t == 44:
#         return [4, 11, 16, 23]
#     elif t == 48 or t == 52 or t == 56 or t == 60:
#         return [6, 10, 15, 21]


# From https://eprint.iacr.org/2004/264.pdf Table 3, pg 20
# Apprently this how you calculate f[t] in the first 16 rounds
def get_ft_16(hash, t):
    Q = hash.get_Q()
    # !!!! Should be equal to hash.get_F()[t]
    return (Q[t] & Q[t-1]) ^ ((Q[t] ^ 0xffffffff) & Q[t-2])

# From https://eprint.iacr.org/2004/264.pdf Table 6, pg 42
def get_ft_32(hash, t):
    Q = hash.get_Q()
    return (Q[t] & Q[t-2]) ^ ((Q[t-2] ^ 0xffffffff) & Q[t-1])

# From https://eprint.iacr.org/2004/264.pdf Table 7, pg 51
def get_ft_48(hash, t):
    Q = hash.get_Q()
    return Q[t] ^ Q[t-1] ^ Q[t-2]

# https://eprint.iacr.org/2004/264.pdf - pg 52
def get_ft_64(hash, t):
    return False # TODO: This is probablisitic, so idk


# See Table 2-4, pg 28 from thesis
def wang_first_16_bitconditions(Q):
    def ones(t, indexes):
        list = [Q[t][i] == 1 for i in indexes]
        return not False in list
    
    def zeroes(t, indexes):
        list = [Q[t][i] == 0 for i in indexes]
        return not False in list

    def hats(t, indexes):
        list = [Q[t][i] == Q[t-1][i] for i in indexes]
        return not False in list

    good = False
    print("Checking the Wang's bitconditions for the first 16 rounds...")
    for t in range(3, 16):
        if t == 3:
            if zeroes(t, [12, 20, 25]): continue
            else: return False
        elif t == 4:
            ones = ones(t, [0, 12, 20])
            zeroes = zeroes(t, [8, 25])
            hats = hats(t, [9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 5:
            ones = ones(t, [0, 4, 9, 26, 29, 31])
            zeroes = zeroes(t, [6, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
            if ones and zeroes: continue
            else: return False
        elif t == 6:
            ones = ones(t, [6, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 25, 31])
            zeroes = zeroes(t, [0, 1, 2, 3, 4, 5, 8, 17, 22, 23, 24, 26, 27, 29])
            hats = hats(t, [7, 28, 30])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 7:
            ones = ones(t, [6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 26])
            zeroes = zeroes(t, [0, 1, 2, 3, 4, 5, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30])
            if ones and zeroes: continue
            else: return False
        elif t == 8:
            ones = ones(t, [7, 8, 11, 15, 21, 23, 25])
            zeroes = zeroes(t, [0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 16, 18, 20, 22, 24, 26, 27, 28, 29, 30, 31])
            if ones and zeroes: continue
            else: return False
        elif t == 9:
            ones = ones(t, [0, 1, 2, 3, 4, 6, 7, 11, 18, 20, 21, 22, 23, 26, 27, 28, 29, 31])
            zeroes = zeroes(t, [5, 12, 13, 14, 15, 16, 24, 25, 30])
            hats = hats(t, [19])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 10:
            ones = ones(t, [1, 11, 12, 13, 14, 15, 16, 17, 19, 25])
            zeroes = zeroes(t, [0, 8, 18, 23, 24, 30, 31])
            if ones and zeroes: continue
            else: return False
        elif t == 11:
            ones = ones(t, [15, 16, 17, 24, 25, 30])
            zeroes = zeroes(t, [0, 1, 12, 13, 14, 18, 19, 23, 31])
            if ones and zeroes: continue
            else: return False
        elif t == 12:
            ones = ones(t, [12, 19, 23])
            zeroes = zeroes(t, [0, 1, 13, 14, 15, 16, 17, 18, 24])
            hats = hats(t, [6, 7])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 13:
            ones = ones(t, [1, 7, 12, 13, 14, 15, 16, 17, 18, 28])
            zeroes = zeroes(t, [0, 6, 23, 24])
            if ones and zeroes: continue
            else: return False
        elif t == 14:
            ones = ones(t, [12, 14, 15, 16, 17, 18, 23, 24, 28])
            zeroes = zeroes(t, [0, 2, 6, 7, 13])
            if ones and zeroes: continue
            else: return False
        elif t == 15:
            ones = ones(t, [2, 7, 16])
            zeroes = zeroes(t, [0, 6, 28])
            if ones and zeroes: return True
            else: return False
        
def botconditions17to64(Q):
    def ones(t, indexes):
        list = [Q[t][i] == 1 for i in indexes]
        return not False in list

    def zeroes(t, indexes):
        list = [Q[t][i] == 0 for i in indexes]
        return not False in list

    def hats(t, indexes):
        list = [Q[t][i] == Q[t - 1][i] for i in indexes]
        return not False in list

    def m(t, indexes):
        list = [Q[t][i] == Q[t - 2][i] for i in indexes]
        return not False in list
    def tag(t, indexes):
        list = [Q[t][i] == (-Q[t - 2][i]) for i in indexes]
        return not False in list

    print("Checking the Wang's bitconditions for the 16->64 rounds...")
    for t in range(16, 64):
        if t == 16:
            ones = ones(t, [2])
            zeroes = zeroes(t, [0])
            if ones and zeroes: continue
            else: return False
        elif t == 17:
            zeroes = zeroes(t, [0,14])
            hats = hats(t,[16, 28])
            if zeroes and hats: continue
            else: return False
        elif t == 18:
            ones = ones(t, [13])
            zeroes = zeroes(t, [0])
            hats = hats(t, [2])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 19:
            zeroes = zeroes(t, [0,13])
            if zeroes: continue
            else: return False
        elif t == 20:
            zeroes = zeroes(t, [0])
            if zeroes: continue
            else: return False
        elif t == 21:
            zeroes = zeroes(t, [0])
            hats = hats(t, [13])
            if zeroes and hats: continue
            else: return False
        elif t == 22:
            zeroes = zeroes(t, [0])
            if zeroes: continue
            else: return False
        elif t == 23:
            zeroes = zeroes(t, [0])
            if zeroes: continue
            else: return False
        elif t == 24:
            ones = ones(t, [1])
            if ones: continue
            else: return False
        elif t >= 25 and t <= 47:
            continue
        elif t == 48:
            m = m(t,[0])
            if m: continue
            else: return False
        elif t == 49:
            m = m(t,[0])
            if m: continue
            else: return False
        elif t == 50:
            tag = tag(t,[0])
            if tag: continue
            else: return False
        elif t >= 51 and t<= 59:
            m = m(t,[0])
            if m: continue
            else: return False
        elif t == 60:
            tag = tag(t, [0])
            zeroes = zeroes(t, [6])
            if tag and zeroes: continue
            else: return False
        elif t == 61:
            tag = tag(t, [0])
            ones = ones(t, [6])
            if tag and ones: continue
            else: return False
        elif t == 62:
            m = m(t,[0])
            zeroes = zeroes(t, [6])
            if m and zeroes: continue
            else: return False
        elif t == 63:
            m = m(t,[0])
            zeroes = zeroes(t,[6])
            if m and zeroes: continue
            else: return False
        elif t == 64:
            continue;

    return True;




# Once we can validate the first 16 Qs, we can produce the corresponding message words, according to the formula from pg 25 of the thesis
# I think this reverses the some MD5 steps, but I'm not sure
def wang_message_words(hash):
    Q = hash.get_Q()
    message_words = []
    for t in range(3, 16):
        rr = RR(modular_sub(Q[t+1], Q[t]), RC[t])
        ft = get_ft_16(hash, t)
        word = modular_sub(rr, ft)
        word = modular_sub(word, Q[t-3])
        word = modular_sub(word, get_AC[t])
        message_words.append(word)
    return message_words

# taken from https://eprint.iacr.org/2004/264.pdf - pg 6, Table 1- The first block of the differential
# will fill all the diferentials accordingly with the values that will be later use to compare the difference between the blocks
def first_block_differential():
    # sigmaX = X1 -X2 # TODO: make a function for each sigma of the values X, T, W, ...
    # sigmaT[t] = modular_add(modular_add(sigmaf(t, Q[t], Q[t-1], Q[t-2]), sigmaQ[t-3]), sigmaW[t])



#helper function that calculates the add-differences
#def sigma(X):
# return modular_sub(X(msgBloc1, t), X(msgBloc2, t))

# def get_differences(hash, hash_prime):
#     Q = hash.get_Q()
#     Q_prime = hash_prime.get_Q()
#     F = hash.get_F()
#     F_prime = hash_prime.get_F()
#     T = hash.get_T()
#     T_prime = hash_prime.get_T()
#     w = 0 # TODO: Figure this out
#     w_prime = 0 # TODO: Figure this out
#     differences = []
#     for t in range(0, 64):
#         rc = get_RC(t)

#         delta_Q = []
#         for i in range(len(Q[t])):
#             delta_Q.append((Q_prime[t][i] - Q[t][i]) % 2)

        
#         delta_Q = bsdr_naf(delta_Q)
        
#         delta_F = F_prime[t] - F[t]
#         delta_w = 0 # TODO: Figure this out
#         delta_T = T_prime[t] - T[t]

#         differences.append({'Q': delta_Q, 'F': delta_F, 'w': delta_w, 'T': delta_T, 'RC': rc})

#     return differences

# def check_differences(d, dq, df, dw, dt, rc):
#     if d['Q'] != d or d['F'] != df or d['w'] != dw or d['T'] != dt or d['RC'] != rc:
#         return False
#     return True


# # Generate a list of values -1 to 1, where items with indices in positive are 1, and in negative are -1
# # 1 => bit at pos x has to match, -1 => bit at pos x has to be different, 
# def diff_list(positive = [], negative = []):
#     lst = [0] * 32
#     for pos in positive: 
#         lst[pos] = 1
#     for neg in negative:
#         lst[neg] = -1
#     return lst

# # Table 2-3, pg 27 in the thesis.
def wang_first_path(hash, hash_prime):
    diff = get_differences(hash, hash_prime)
    for t in range(64):
        d = diff[t]
        rc = get_RC(t)
        # TODO: Check if there is no message modification when the a condition fails
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
            if not correct:
                return (False, t)
        elif t == 5:
            q_diffs = diff_list(range(6, 22), [22])
            f_diffs = modular_add(2**11, 2**19)
            t_diffs = modular_add(2**11, 2**19)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 12)
            if not correct:
                return (False, t)
        elif t == 6:
            q_diffs = [6,23,31]
            f_diffs = modular_add(-2**10, -2**14)
            t_diffs = modular_add(-2**10, -2**14)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 17)
            if not correct:
                return (False, t)
        elif t == 7:
            q = [range(0,4),range(6,10), range(26, 31)]
            negq = [5, 11, 23, 25]
            q_diffs = diff_list(q,negq)
            f_diffs = modular_add(modular_add(modular_add(-2**2, 2**5), modular_add(2**10, 2**16)), modular_add(-2**25, -2**27))
            t_diffs = modular_add(modular_add(modular_add(-2**2, 2**5), modular_add(2**10, 2**16)), modular_add(-2**25, -2**27))
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 22)
            if not correct:
                return (False, t)
        elif t == 8:
            q = [0, 15, 17, 18, 19]
            negq = [16, 20, 23]
            q_diffs = diff_list(q, negq)
            f_diffs = modular_add(modular_add(modular_add(2**6, 2**8), modular_add(2 ** 10, 2 ** 16)),
                                  modular_add(-2**24, 2**31))
            t_diffs = modular_add(modular_add(2**8, modular_add(2**10, 2**16)),
                                  modular_add(-2**24, 2**31))
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 7)
            if not correct:
                return (False, t)
        elif t == 9:
            q = [1, 6, 7]
            negq = [0, 8, 31]
            q_diffs = diff_list(q, negq)
            f_diffs = modular_add(modular_add(modular_add(2**0, 2**6), modular_add(-2**20, -2**23)),
                                  modular_add(2**26, 2**31))
            t_diffs = modular_add(modular_add(2**0, -2**20),2**26)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 12)
            if not correct:
                return (False, t)
        elif t == 10:
            q = [13, 31]
            negq = [12]
            q_diffs = diff_list(q, negq)
            f_diffs = modular_add(modular_add(2**0, 2**6), modular_add(2**13, -2**23))
            t_diffs = modular_add(2**13, -2**26)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 17)
            if not correct:
                return (False, t)
        elif t == 11:
            q_diffs = [30,31]
            f_diffs = modular_add(-2**0, -2**8)
            t_diffs = modular_add(modular_add(2**8, 2**17), -2**23)
            correct = check_differences(d, q_diffs, f_diffs, 2**15, t_diffs, 22)
            if not correct:
                return (False, t)
        elif t == 12:
            q = [7, 13, 14, 15, 16, 17, 18, 31]
            negq = [8, 19]
            q_diffs = diff_list(q, negq)
            f_diffs = modular_add(modular_add(2**7, 2**17), 2**31)
            t_diffs = modular_add(modular_add(2**0, 2**6), 2**17)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 7)
            if not correct:
                return (False, t)
        elif t == 13:
            q = [25,31]
            negq = [24]
            q_diffs = diff_list(q, negq)
            f_diffs = modular_add(-2**13, -2**31)
            correct = check_differences(d, q_diffs, f_diffs, 0, -2**12, 12)
            if not correct:
                return (False, t)
        elif t == 14:
            q_diffs = [31]
            f_diffs = modular_add(2**18, 2**31)
            t_diffs = modular_add(2**18, -2**30)
            correct = check_differences(d, q_diffs, f_diffs, 2**31, t_diffs, 17)
            if not correct:
                return (False, t)
        elif t == 15:
            q = [3, 31]
            negq = [15]
            q_diffs = diff_list(q, negq)
            f_diffs = modular_add(2**25, 2**31)
            t_diffs = modular_add(modular_add(-2**7, -2**13), 2**25)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs, 22)
            if not correct:
                return (False, t)
        elif t == 16:
            q = [31]
            negq = [29]
            q_diffs = diff_list(q, negq)
            correct = check_differences(d, q_diffs, 2**31, 0, 2**24, 5)
            if not correct:
                return (False, t)
        elif t == 17:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, 9)
            if not correct:
                return (False, t)
        elif t == 18:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 2**15, 2**3, 14)
            if not correct:
                return (False, t)
        elif t == 19:
            q_diffs = [17,31]
            correct = check_differences(d, q_diffs, 2**31, 0, -2**29, 20)
            if not correct:
                return (False, t)
        elif t == 20:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, 5)
            if not correct:
                return (False, t)
        elif t == 21:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, 9)
            if not correct:
                return (False, t)
        elif t == 22:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 0, 2**17, 14)
            if not correct:
                return (False, t)
        elif t == 23:
            correct = check_differences(d, 0, 0, 2**31, 0, 20)
            if not correct:
                return (False, t)
        elif t == 24:
            correct = check_differences(d, 0, 2**31, 2**31, 0, 5)
            if not correct:
                return (False, t)
        elif t == 25:
            correct = check_differences(d, 0, 0, 2**31, 0, 9)
            if not correct:
                return (False, t)
        elif t >= 26 and t <= 33:
            correct = check_differences(d, 0, 0, 0, 0, rc)
            if not correct:
                return (False, t)
        elif t == 34:
            correct = check_differences(d, 0, 0, 2**15, 2**15, 16)
            if not correct:
                return (False, t)
        elif t == 35:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 2**31, 0, 23)
            if not correct:
                return (False, t)
        elif t == 36:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 0, 0, 0, 4)
            if not correct:
                return (False, t)
        elif t == 37:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 2**31, 0, 11)
            if not correct:
                return (False, t)
        elif t >= 38 and t <= 49:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, rc)
            if not correct:
                return (False, t)
        elif t == 50:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 0, 2**31, 0, 15)
            if not correct:
                return (False, t)
        elif t >= 51 and t <= 59:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, rc)
            if not correct:
                return (False, t)
        elif t == 60:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 0, 2**31, 0, 6)
            if not correct:
                return (False, t)
        elif t == 61:
            q_diffs = [31]
            correct = check_differences(d, q_diffs, 2**31, 2**15, 2**15, 10)
            if not correct:
                return (False, t)
        elif t == 62:
            q_diffs = [31, 25]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, 15)
            if not correct:
                return (False, t)
        elif t == 63:
            q_diffs = [31, 25]
            correct = check_differences(d, q_diffs, 2**31, 0, 0, 21)
            if not correct:
                return (False, t)
        elif t == 64:
            #probably empty, there are some x in the table for most things
            continue;

    return (True, -1)




