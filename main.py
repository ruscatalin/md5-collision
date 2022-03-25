import gui
import md51
# from md51 import *
from util import *
import secrets
import string


alphabet = string.ascii_letters
## two 512-bit messages: one should be fixed, one should be changed
# # M1 will be a random message of 512 random bits. Use secrets to generate the random bits.
M1 = ''.join(secrets.choice(alphabet) for i in range(16))
M2 = 'Hello Hello'




def write_to_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
        f.close()
    

def start_cracking():
    global M1, M2

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
    
    # gui.update_output('Collision found: {}'.format(M1))
    # gui.button_switch()


if __name__ == '__main__':

    from bitarray import bitarray

    # gui.start_app()
    # start_cracking()
    generated_Qs = generate_first16_Qs()
    message = generate_message_from_Qs(generated_Qs)
    # convert each element of message to bytes and then to string
    stringed = []
    for m in message:
        #convert m to bytes
        m_bytes = m.to_bytes(4, byteorder='big')
        stringed.append(m_bytes)

    concatenated_bytes = b''.join(stringed)

    hM1 = md51.hash(concatenated_bytes)
    Q = md51.Q
    

    # Start cracking from here:...

    # print(hash(b"177"))
    


