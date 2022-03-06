from calendar import c
import random
from re import M, S, U
from tkinter import Y

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