import secrets
from util import *


# # Table 2-3, pg 27 in the thesis.
def wang_first_path(hash, hash_prime):
    diff = get_differences(hash, hash_prime)
    for t in range(64):
        d = diff[t]

        if t <= 3:
            #Example for 0 <= t <= 3:
            #dQt = 0, dFt = 0, dwt = 0, dT=0
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 0, 0, 0)
            if not correct:
                return (False, t)
        elif t == 4:
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 0, 2**31, 2**31)
            if not correct:
                return (False, t)
        elif t == 5:
            posq = [i for i in range(6, 22)]
            q_diffs = generate_bsdr(posq, [22])
            f_diffs = modular_add(2**11, 2**19)
            t_diffs = modular_add(2**11, 2**19)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 6:
            q_diffs = generate_bsdr([6,23,31])
            f_diffs = modular_add(-2**10, -2**14)
            t_diffs = modular_add(-2**10, -2**14)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 7:
            posq = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 26, 27, 28, 29, 30, 31]
            negq = [5, 11, 23, 25]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(-2**2, 2**5), modular_add(2**10, 2**16)), modular_add(-2**25, -2**27))
            t_diffs = modular_add(modular_add(modular_add(-2**2, 2**5), modular_add(2**10, 2**16)), modular_add(-2**25, -2**27))
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 8:
            posq = [0, 15, 17, 18, 19]
            negq = [16, 20, 23]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(2**6, 2**8), modular_add(2 ** 10, 2 ** 16)),
                                  modular_add(-2**24, 2**31))
            t_diffs = modular_add(modular_add(2**8, modular_add(2**10, 2**16)),
                                  modular_add(-2**24, 2**31))
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 9:
            posq = [1, 6, 7]
            negq = [0, 8, 31]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(2**0, 2**6), modular_add(-2**20, -2**23)),
                                  modular_add(2**26, 2**31))
            t_diffs = modular_add(modular_add(2**0, -2**20),2**26)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 10:
            posq = [13, 31]
            negq = [12]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(2**0, 2**6), modular_add(2**13, -2**23))
            t_diffs = modular_add(2**13, -2**26)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 11:
            q_diffs = generate_bsdr([30,31])
            f_diffs = modular_add(-2**0, -2**8)
            t_diffs = modular_add(modular_add(2**8, 2**17), -2**23)
            correct = check_differences(d, q_diffs, f_diffs, 2**15, t_diffs)
            if not correct:
                return (False, t)
        elif t == 12:
            posq = [7, 13, 14, 15, 16, 17, 18, 31]
            negq = [8, 19]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(2**7, 2**17), 2**31)
            t_diffs = modular_add(modular_add(2**0, 2**6), 2**17)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 13:
            posq = [25,31]
            negq = [24]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(-2**13, -2**31)
            correct = check_differences(d, q_diffs, f_diffs, 0, -2**12)
            if not correct:
                return (False, t)
        elif t == 14:
            q_diffs = generate_bsdr([31])
            f_diffs = modular_add(2**18, 2**31)
            t_diffs = modular_add(2**18, -2**30)
            correct = check_differences(d, q_diffs, f_diffs, 2**31, t_diffs)
            if not correct:
                return (False, t)
        elif t == 15:
            posq = [3, 31]
            negq = [15]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(2**25, 2**31)
            t_diffs = modular_add(modular_add(-2**7, -2**13), 2**25)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 16:
            posq = [31]
            negq = [29]
            q_diffs = generate_bsdr(posq, negq)
            correct = check_differences(d, q_diffs, 2**31, 0, 2**24)
            if not correct:
                return (False, t)
        elif t == 17:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 18:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 2**15, 2**3)
            if not correct:
                return (False, t)
        elif t == 19:
            q_diffs = generate_bsdr([17, 31])
            correct = check_differences(d, q_diffs, 2**31, 0, -2**29)
            if not correct:
                return (False, t)
        elif t == 20:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 21:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 22:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 2**17)
            if not correct:
                return (False, t)
        elif t == 23:
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 0, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 24:
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 2**31, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 25:
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 0, 2**31, 0)
            if not correct:
                return (False, t)
        elif t >= 26 and t <= 33:
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 0, 0, 0)
            if not correct:
                return (False, t)
        elif t == 34:
            q_diffs = generate_bsdr()
            correct = check_differences(d, q_diffs, 0, 2**15, 2**15)
            if not correct:
                return (False, t)
        elif t == 35 or t == 37:
            q_diffs = [2**31]
            correct = check_differences(d, q_diffs, 2**31, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 36:
            q_diffs = [2**31]
            correct = check_differences(d, q_diffs, 0, 0, 0)
            if not correct:
                return (False, t)
        elif (t >= 38 and t <= 49) or (t >= 51 and t <= 59):
            q_diffs = [2**31]
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 50 or t == 60:
            q_diffs = [2**31]
            correct = check_differences(d, q_diffs, 0, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 61:
            q_diffs = [2**31]
            correct = check_differences(d, q_diffs, 2**31, 2**15, 2**15)
            if not correct:
                return (False, t)
        elif t == 62 or t == 63:
            q_diffs = [modular_add(2**31, 2**25)]
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif d['Q'] == [modular_add(2**31, 2**25)]:
            return (True, -1)
        else:
            return (False, t)

# Table 2-5, pg 29 in thesis
def wang_second_path(hash, hash_prime):
    diff = get_differences(hash, hash_prime)
    for t in range(64):
        d = diff[t]

        if t == 0:
            q_diffs = generate_bsdr([25, 31])
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 1:
            q_diffs = generate_bsdr([25, 31])
            correct = check_differences(d, q_diffs, 2**31, 0, 2**25)
            if not correct:
                return (False, t)
        elif t == 2:
            q_diffs = generate_bsdr([5, 25, 31])
            t_diffs = modular_add(2**31, 2**26)
            correct = check_differences(d, q_diffs, 2**25, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 3:
            posq = [7, 12, 21, 30, 31]
            negq = [5, 6, 11, 16, 17, 18, 19, 20, 25, 26, 27, 28, 29]
            q_diffs = generate_bsdr(posq, negq) 
            f_diffs = modular_add(modular_add(modular_sub(-2**11, 2**21), modular_sub(2**25, 2**27)), 2**31)
            t_diffs = modular_add(modular_add(-2**11, -2**21), -2**26)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 4:
            posq = [1, 2, 3, 5, 26, 31]
            negq = [4, 25]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(modular_add(2**1, -2**3), -2**18), 2**26), 2**30)
            w_diffs = 2**31
            t_diffs = modular_add(modular_add(modular_add(modular_add(modular_add(2**1, 2**2), -2**18), 2**25), 2**26), 2**30)
            correct = check_differences(d, q_diffs, f_diffs, w_diffs, t_diffs)
            if not correct:
                return (False, t)
        elif t == 5:
            posq = [0, 7, 8, 12, 31]
            negq = [6, 9, 10, 11]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(modular_add(modular_add(modular_add
                        (modular_add(-2**4, -2**5), -2**8), -2**20), -2**25), -2**26), 2**28), 2**30)
            t_diffs = modular_add(modular_add(modular_add(modular_add(modular_add(-2**4, -2**8), -2**20), -2**26), 2**28), -2**30)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 6:
            posq = [16, 20, 31]
            negq = [17, 21]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(modular_add(modular_add
                        (modular_add(2**3, -2**5), -2**10), -2**11), -2**16), -2**21), -2**25)
            t_diffs = modular_add(modular_add(modular_add(2**3, -2**10), -2**21), -2**31)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 7:
            posq = [6, 7, 8, 27, 31]
            negq = [9, 28]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(2**16, -2**27), 2**31)
            t_diffs = modular_add(modular_add(modular_add(modular_add(-2**1, 2**5), 2**16), 2**25), -2**27)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 8:
            posq = [16, 23, 24, 25, 31]
            negq = [15, 17, 26]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(-2**6, 2**16), 2**25)
            t_diffs = modular_add(modular_add(modular_add(modular_add(modular_add(2**0, 2**8), 2**9), 2**16), 2**25), -2**31)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 9:
            posq = [1, 9, 31]
            negq = [0, 6, 7, 8]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(modular_add(modular_add(2**0, 2**16), -2**26), 2**31)
            t_diffs = modular_add(modular_add(2**0, -2**20), -2**26)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 10:
            q_diffs = generate_bsdr([12, 31])
            f_diffs = modular_add(2**6, 2**31)
            correct = check_differences(d, q_diffs, f_diffs, 0, -2**27)
            if not correct:
                return (False, t)
        elif t == 11:
            q_diffs = generate_bsdr([31])
            t_diffs = modular_add(-2**17, -2**23)
            correct = check_differences(d, q_diffs, 2**31, -2**15, t_diffs)
            if not correct:
                return (False, t)
        elif t == 12:
            posq = [13, 14, 15, 16, 17, 18, 31]
            negq = [7, 19]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(2**17, 2**31)
            t_diffs = modular_add(modular_add(2**0, 2**6), 2**17)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 13:
            posq = [30, 31]
            negq = [24, 25, 26, 27, 28, 29]
            q_diffs = generate_bsdr(posq, negq)
            f_diffs = modular_add(-2**13, 2**31)
            correct = check_differences(d, q_diffs, f_diffs, 0, -2**12)
            if not correct:
                return (False, t)
        elif t == 14:
            q_diffs = generate_bsdr([31])
            f_diffs = modular_add(2**18, 2**30)
            t_diffs = f_diffs
            correct = check_differences(d, q_diffs, f_diffs, 2**31, t_diffs)
            if not correct:
                return (False, t)
        elif t == 15:
            q_diffs = generate_bsdr([3, 15, 31])
            f_diffs = modular_add(-2**25, 2**31)
            t_diffs = modular_add(modular_add(-2**7, -2**13), -2**25)
            correct = check_differences(d, q_diffs, f_diffs, 0, t_diffs)
            if not correct:
                return (False, t)
        elif t == 16:
            q_diffs = generate_bsdr([31], [29])
            correct = check_differences(d, q_diffs, 2**31, 0, 2**24)
            if not correct:
                return (False, t)
        elif t == 17:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 18:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, -2**15, 2**3)
            if not correct:
                return (False, t)
        elif t == 19:
            q_diffs = generate_bsdr([17, 31])
            correct = check_differences(d, q_diffs, 2**31, 0, -2**29)
            if not correct:
                return (False, t)
        elif t == 20 or t == 21:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t == 22:
            q_diffs = generate_bsdr([31])
            correct = check_differences(d, q_diffs, 2**31, 0, 2**17)
            if not correct:
                return (False, t)
        elif t == 23 or t == 25:
            correct = check_differences(d, generate_bsdr(), 0, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 24:
            correct = check_differences(d, generate_bsdr(), 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif t >= 26 or t <= 33:
            correct = check_differences(d, generate_bsdr(), 0, 0, 0)
            if not correct:
                return (False, t)
        elif t == 34:
            correct = check_differences(d, generate_bsdr(), 0, -2**15, -2**15)
            if not correct:
                return (False, t)
        elif t == 35 or t == 37:
            q_diffs = [2**31]  # no bsdr is needed from now because we check the sigma, not the delta
            correct = check_differences(d, q_diffs, 2**31, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 36:
            correct = check_differences(d, [2**31], 0, 0, 0)
            if not correct:
                return (False, t)
        elif (t >= 38 and t <= 49) or (t >= 51 and t <= 59):
            correct = check_differences(d, [2**31], 0, 0, 0)
            if not correct:
                return (False, t)
        elif t == 50 or t == 60:
            correct = check_differences(d, [2**31], 0, 2**31, 0)
            if not correct:
                return (False, t)
        elif t == 61:
            correct = check_differences(d, [2**31], 2**31, -2**15, -2**15)
            if not correct:
                return (False, t)
        elif t == 62 or t == 63:
            q_diffs = modular_add(2**31, -2**25)
            correct = check_differences(d, q_diffs, 2**31, 0, 0)
            if not correct:
                return (False, t)
        elif d['Q'] == [modular_add(2**31, -2**25)]:  # this is round 64
            return (True, -1)
        else:
            return (False, t)
            

def fill_Q(t):
    random_int = secrets.randbits(32)
    result = list("{:032b}".format(random_int))
    
    def fill_zeroes(indexes):
        for i in indexes:
            result[31 - i] = '0'
    def fill_ones(indexes):
        for i in indexes:
            result[31 - i] = '1'
    
    if t == 3:
        fill_zeroes([12, 20, 25])
    elif t == 4:
        fill_zeroes([8, 25])
        fill_ones([0, 12, 20])
    elif t == 5:
        fill_ones([0, 4, 9, 26, 29, 31])
        fill_zeroes([6, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
    elif t == 6:
        fill_ones([6, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 25, 31])
        fill_zeroes([0, 1, 2, 3, 4, 5, 8, 17, 22, 23, 24, 26, 27, 29])
    elif t == 7:
        fill_ones([6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 26])
        fill_zeroes([0, 1, 2, 3, 4, 5, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30])
    elif t == 8:
        fill_ones([7, 8, 11, 15, 21, 23, 25])
        fill_zeroes([0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 16, 18, 20, 22, 24, 26, 27, 28, 29, 30, 31])
    elif t == 9:
        fill_ones([0, 1, 2, 3, 4, 6, 7, 11, 18, 20, 21, 22, 23, 26, 27, 28, 29, 31])
        fill_zeroes([5, 12, 13, 14, 15, 16, 24, 25, 30])
    elif t == 10:
        fill_ones([1, 11, 12, 13, 14, 15, 16, 17, 19, 25])
        fill_zeroes([0, 8, 18, 23, 24, 30, 31])
    elif t == 11:
        fill_ones([15, 16, 17, 24, 25, 30])
        fill_zeroes([0, 1, 12, 13, 14, 18, 19, 23, 31])
    elif t == 12:
        fill_ones([12, 19, 23])
        fill_zeroes([0, 1, 13, 14, 15, 16, 17, 18, 24])
    elif t == 13:
        fill_ones([1, 7, 12, 13, 14, 15, 16, 17, 18, 28])
        fill_zeroes([0, 6, 23, 24])
    elif t == 14:
        fill_ones([12, 14, 15, 16, 17, 18, 23, 24, 28])
        fill_zeroes([0, 2, 6, 7, 13])
    elif t == 15:
        fill_ones([2, 7, 16])
        fill_zeroes([0, 6, 28])

    return ''.join(result)


def fill_Q_second_block(first_block_Q, t):
    random_int = secrets.randbits(32)
    result = list("{:032b}".format(random_int))
    
    def fill_zeroes(indexes):
        for i in indexes:
            result[31 - i] = '0'
    def fill_ones(indexes):
        for i in indexes:
            result[31 - i] = '1'

    if t == -2:
        result = first_block_Q[-3]
        fill_zeroes([6])
    elif t == -1:
        result = first_block_Q[-2]
        fill_ones([6])
        fill_zeroes([5])
    elif t == 0:
        result = first_block_Q[-1]
        fill_zeroes([5, 6, 26])
    elif t == 1:
        fill_zeroes([4, 6, 20, 26])
        fill_ones([5, 10, 25])
    elif t == 2:
        fill_zeroes([6, 10, 15, 26, 29, 30])
        fill_ones([4, 5, 20, 26])
    elif t == 3:
        fill_zeroes([1, 10, 19, 24])
        fill_ones([2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 20, 23, 25, 26, 29, 30])
    elif t == 4:
        fill_zeroes([1, 5, 10, 11, 12, 14, 15, 19, 20, 23, 24, 25, 26, 28, 29, 30])
        fill_ones([2, 3, 4, 6, 13, 27])
    elif t == 5:
        fill_zeroes([2, 3, 5, 11, 19, 23, 24, 26, 28, 29, 30, 31])
        fill_ones([1, 4, 10, 12, 13, 14, 15, 20, 21, 22, 25, 27])
    elif t == 6:
        fill_zeroes([3, 4, 6, 11, 15, 19, 22, 23, 24, 26, 28, 31])
        fill_ones([5, 8, 10, 14, 16, 20, 21, 25, 27, 29, 30])
    elif t == 7:
        fill_zeroes([4, 10, 11, 14, 23, 24, 25])
        fill_ones([3, 5, 6, 15, 16, 19, 20, 21, 22, 31])
    elif t == 8:
        fill_zeroes([3, 4, 6, 7, 8, 15, 31])
        fill_ones([5, 10, 11, 14, 16, 22, 23, 24, 25])
    elif t == 9:
        fill_zeroes([6, 7, 8, 14, 16, 22, 30])
        fill_ones([3, 4, 5, 15, 23, 24, 25, 31])
    elif t == 10:
        fill_zeroes([13, 18, 19, 30, 31])
        fill_ones([5, 6, 7, 8, 14, 15, 16, 17, 22, 23, 24, 25])
    elif t == 11:
        fill_zeroes([14, 18, 19])
        fill_ones([13, 15, 16, 17, 22, 23, 24, 25, 30, 31])
    elif t == 12:
        fill_zeroes([13, 14, 15, 16, 17, 18, 19])
        fill_ones([12, 20, 24])
    elif t == 13:
        fill_zeroes([1, 24])
        fill_ones([2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 28])
    elif t == 14:
        fill_zeroes([2, 3, 4, 5, 6, 7, 13])
        fill_ones([1, 12, 14, 15, 16, 17, 18, 24, 28])
    elif t == 15:
        fill_zeroes([0, 6, 16, 28])
        fill_ones([1, 2, 3, 4, 5, 7])

    return ''.join(result)


def generate_first16_Qs():
    def fill_hats(bitstring, indexes, t):
        for i in indexes:
            bitstring[31 - i] = result[t - 1][31 - i]

    result = []
    for t in range(16):
        random_int = secrets.randbits(32)
        result.append(list("{:032b}".format(random_int)))

        if t >= 3:  
            result[t] = list(fill_Q(t))
            if t == 4:
                fill_hats(result[t], [9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24], t)
            elif t == 6:
                fill_hats(result[t], [7, 28, 30], t)
            elif t == 9:
                fill_hats(result[t],[19], t)
            elif t == 12:
                fill_hats(result[t],[6, 7], t)
        result[t] = ''.join(result[t])[::-1]  # reverse the bitstring to big endian

    return result


def generate_first16_Qs_second_block(first_block_Q):
    def fill_hats(bitstring, indexes, t):
        for i in indexes:
            bitstring[31 - i] = result[t - 1][31 - i]

    def fill_exclamation(bitstring, indexes, t):
        for i in indexes:
            bitstring[31 - i] = '0' if result[t - 1][31 - i] == '1' else '1'

    result = []
    for t in range(-2, 16):        
        result.append(fill_Q_second_block(first_block_Q, t))

        if t == -1:
            fill_hats(result[-1], [0], -1)
        elif t == 0:
            fill_hats(result[t], [0], t)
        elif t == 1:
            fill_exclamation(result[t], [0], t)
        elif t == 2:
            fill_hats(result[t], [0, 1, 2, 3, 11, 12, 13, 14, 19, 24], t)
        elif t == 3:
            fill_hats(result[t], [0, 27, 28], t)
        elif t == 4:
            fill_hats(result[t], [0, 21, 22, 31], t)
        elif t == 5:
            fill_exclamation(result[t], [0], t)
        elif t == 6:
            fill_hats(result[t], [0], t)
        elif t == 7:
            fill_hats(result[t], [8], t)
            fill_exclamation(result[t], [0], t)
        elif t == 8:
            fill_hats(result[t], [0, 30], t)
        elif t == 9:
            fill_hats(result[t], [0, 19], t)
        elif t == 10:
            fill_hats(result[t], [0], t)
        elif t == 11:
            fill_hats(result[t], [0, 12], t)
        elif t == 12:
            fill_hats(result[t], [0, 1, 2, 3, 4, 5, 6, 7], t)
        elif t == 13:
            fill_exclamation(result[t], [0], t)
        elif t == 14:
            fill_hats(result[t], [0], t)

        result[t] = ''.join(result[t])[::-1]  # reverse the bitstring

    return result


def bitconditions16to64(Q, exact_step=None):
    Qt, Qtm1 = None, None
    def check_ones(indexes):
        list = [int(Qt[31 - i]) == 1 for i in indexes]
        return not False in list
    def check_zeroes(indexes):
        list = [int(Qt[31 - i]) == 0 for i in indexes]
        return not False in list
    def check_hats(indexes):
        list = [Qt[31 - i] == Qtm1[31 - i] for i in indexes]
        return not False in list
    def check_m(indexes):
        list = [Qt[31 - i] == Qtm2[31 - i] for i in indexes]
        return not False in list
    def check_tag(indexes):
        list = [Qt[31 - i] != Qtm2[31 - i] for i in indexes]
        return not False in list

    if exact_step:
        first_condition, last_condition = exact_step, exact_step
    else:
        first_condition, last_condition = 16, 64
        
    for t in range(first_condition, last_condition):
        Qt      = '{:032b}'.format(Q[t])
        Qtm1    = '{:032b}'.format(Q[t-1])
        Qtm2    = '{:032b}'.format(Q[t-2])
        if t == 16:
            ones    = check_ones([2])
            zeroes  = check_zeroes([0])
            if ones and zeroes: continue
            else: return False
        elif t == 17:
            zeroes  = check_zeroes([0,14])
            hats    = check_hats([16, 28])
            if zeroes and hats: continue
            else: return False
        elif t == 18:
            ones    = check_ones([14])
            zeroes  = check_zeroes([0])
            hats    = check_hats([2])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 19:
            zeroes  = check_zeroes([0, 14])
            if zeroes: continue
            else: return False
        elif t == 20:
            zeroes  = check_zeroes([0])
            if zeroes: continue
            else: return False
        elif t == 21:
            zeroes  = check_zeroes([0])
            hats = check_hats([14])
            if zeroes and hats: continue
            else: return False
        elif t == 22:
            zeroes  = check_zeroes([0])
            if zeroes: continue
            else: return False
        elif t == 23:
            zeroes  = check_zeroes([0])
            if zeroes: continue
            else: return False
        elif t == 24:
            ones    = check_ones([1])
            if ones: continue
            else: return False
        elif t >= 25 and t <= 47:
            continue
        elif t == 48:
            m       = check_m([0])
            if m: continue
            else: return False
        elif t == 49:
            m       = check_m([0])
            if m: continue
            else: return False
        elif t == 50:
            tag     = check_tag([0])
            if tag: continue
            else: return False
        elif t >= 51 and t<= 59:
            print(t)
            m       = check_m([0])
            if m: continue
            else: return False
        elif t == 60:
            tag     = check_tag([0])
            zeroes  = check_zeroes([6])
            if tag and zeroes: continue
            else: return False
        elif t == 61:
            tag     = check_tag([0])
            ones    = check_ones([6])
            if tag and ones: continue
            else: return False
        elif t == 62:
            print(t)
            m       = check_m([0])
            zeroes  = check_zeroes([6])
            if m and zeroes: continue
            else: return False
        elif t == 63:
            print(t)
            m       = check_m([0])
            zeroes  = check_zeroes([6])
            if m and zeroes: continue
            else: return False
        elif t == 64: break

    return True


def bitconditions16to64_second_block(Q):
    Qt, Qtm1 = None, None
    def check_ones(indexes):
        list = [int(Qt[31 - i]) == 1 for i in indexes]
        return not False in list
    def check_zeroes(indexes):
        list = [int(Qt[31 - i]) == 0 for i in indexes]
        return not False in list
    def check_hats(indexes):
        list = [Qt[31 - i] == Qtm1[31 - i] for i in indexes]
        return not False in list
    def check_tag(indexes):
        list = [Qt[31 - i] != Qtm2[31 - i] for i in indexes]
        return not False in list
    def check_m(indexes):
        list = [Qt[31 - i] == Qtm2[31 - i] for i in indexes]
        return not False in list    

    for t in range(16, 64):
        Qt      = '{:032b}'.format(Q[t])
        Qtm1    = '{:032b}'.format(Q[t-1])
        Qtm2    = '{:032b}'.format(Q[t-2])
        if t == 16:
            ones    = check_ones([2])
            zeroes  = check_zeroes([0])
            if ones and zeroes: continue
            else: return False
        elif t == 17:
            zeroes  = check_zeroes([0, 14])
            hats    = check_hats([16, 28])
            if zeroes and hats: continue
            else: return False
        elif t == 18:
            ones    = check_ones([14])
            zeroes  = check_zeroes([0])
            hats    = check_hats([2])
            if ones and zeroes and hats: continue
            else: return False
        elif t == 19:
            zeroes  = check_zeroes([0, 14])
            if zeroes: continue
            else: return False
        elif t == 20:
            zeroes  = check_zeroes([0])
            if zeroes: continue
            else: return False
        elif t == 21:
            zeroes  = check_zeroes([0])
            hats = check_hats([14])
            if zeroes and hats: continue
            else: return False
        elif t == 22:
            zeroes  = check_zeroes([0])
            if zeroes: continue
            else: return False
        elif t == 23:
            zeroes  = check_zeroes([0])
            if zeroes: continue
            else: return False
        elif t == 24:
            ones    = check_ones([1])
            if ones: continue
            else: return False
        elif t >= 25 and t <= 47:
            continue
        elif t == 48:
            m       = check_m([0])
            if m: continue
            else: return False
        elif t == 49:
            m       = check_m([0])
            if m: continue
            else: return False
        elif t == 50:
            tag     = check_tag([0])
            if tag: continue
            else: return False
        elif t >= 51 and t<= 59:
            m       = m([0])
            if m: continue
            else: return False
        elif t == 60:
            tag     = check_tag([0])
            zeroes  = check_zeroes([6])
            if tag and zeroes: continue
            else: return False
        elif t == 61:
            tag     = check_tag([0])
            ones    = check_ones([6])
            if tag and ones: continue
            else: return False
        elif t == 62:
            m       = check_m([0])
            zeroes  = check_zeroes([6])
            if m and zeroes: continue
            else: return False
        elif t == 63:
            m       = check_m([0])
            zeroes  = check_zeroes([6])
            if m and zeroes: continue
            else: return False
        elif t == 64: continue

    return True



