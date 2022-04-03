import math

rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

Q = []
F = []
T = []
R = []

message = None

functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
            16 * [lambda b, c, d: (d & b) | (~d & c)] + \
            16 * [lambda b, c, d: b ^ c ^ d] + \
            16 * [lambda b, c, d: c ^ (b | ~d)]

index_functions = 16 * [lambda i: i] + \
                  16 * [lambda i: (5 * i + 1) % 16] + \
                  16 * [lambda i: (3 * i + 5) % 16] + \
                  16 * [lambda i: (7 * i) % 16]


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message):
    global Q, F, T, R
    Q = []
    F = []
    T = []
    R = []
    message = bytearray(message)  # copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')

    hash_pieces = init_values[:]
    
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        
        chunk = message[chunk_ofst:chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            F.append(f)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            T.append(to_rotate)
            R.append(left_rotate(to_rotate, rotate_amounts[i]))
            new_b = (b + R[-1]) & 0xFFFFFFFF
            Q.append(new_b)
            a, b, c, d = d, new_b, b, c
            
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

 

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))


def md5_one_step(which_step, second_block=False, final_step=False):
    global message, Q, F, T, R

    message = bytearray(message)
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    if 0x80 not in message:
        message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')

    if len(Q) < 4:
        a, b, c, d = init_values
    else:
        li = []
        for q in Q[-4:]:
            if isinstance(q, int):
                li.append(q)
            else:
                li.append(int(q, 2))
        a, b, c, d = li

    # do one step of the md5 algorithm
    if second_block:
        chunk = message[64:128]
    else:
        chunk = message[0:64]
    f = functions[which_step](b, c, d)
    F.append(f)
    g = index_functions[which_step](which_step)
    to_rotate = a + f + constants[which_step] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
    T.append(to_rotate)
    R.append(left_rotate(to_rotate, rotate_amounts[which_step]))
    new_b = (b + R[-1]) & 0xFFFFFFFF
    Q.append(new_b)
    
    if final_step:
        hash_pieces = []
        for i, val in enumerate([a, b, c, d]):
            hash_pieces.append((val + Q[-(4 - i)]) & 0xFFFFFFFF)
        return sum(x << (32 * i) for i, x in enumerate(hash_pieces))




def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

def hash(message):
    return md5_to_hex(md5(message))


# if __name__ == '__main__':
#     # demo = [b"", b"a", b"abc", b"message digest", b"abcdefghijklmnopqrstuvwxyz",
#     #         b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
#     #         b"12345678901234567890123456789012345678901234567890123456789012345678901234567890"]
#     demo = [b"1020"]
#     for message in demo:
#         print(md5_to_hex(md5(message)), ' <= "', message.decode('ascii'), '"', sep='')