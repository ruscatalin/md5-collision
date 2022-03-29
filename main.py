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

hM0 = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}
hM0_prime = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}
hM1 = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}
hM1_prime = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}


def write_to_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
        f.close()
    

def generate_valid_bytes(second_block=False, first_block_Qs=None):
    if not second_block:
        generated_Qs = generate_first16_Qs()
    else:
        generated_Qs = generate_first16_Qs_second_block(first_block_Qs)
    message = generate_message_from_Qs(generated_Qs)
    concatenated_bytes = int_list_to_concatenated_bytes(message)
    return concatenated_bytes, message


def start_cracking(Qs, message):

    print("Started cracking...")

    m0_diff = [0, 0, 0, 0, 2**31, 0, 0, 0, 0, 0, 0, 2**15, 0, 0, 2**31, 0]
    m1_diff = [0, 0, 0, 0, 2**31, 0, 0, 0, 0, 0, 0, -2**15, 0, 0, 2**31, 0]

    while True:
        if bitconditions16to64(Qs): # Check the remaining bitconditions of block1
            write_to_file('log.txt', '\n 16-64: ' + message)
            m0_prime = [modular_add(message[i], m0_diff[i]) for i in range(16)]
            bytes_m0_prime = int_list_to_concatenated_bytes(m0_prime)
            hM0_prime['hash'] = md51.hash(bytes_m0_prime)
            hM0_prime['Q'] = md51.Q
            hM0_prime['T'] = md51.T
            hM0_prime['F'] = md51.F
            hM0_prime['R'] = md51.R
            hM0_prime['message'] = m0_prime

            first_path_found, step = wang_first_path(hM0, hM0_prime)
            if first_path_found:  # start looking into the second path
                print("First path found!")
                second_path_found = False
                while True:
                    bytes, m1 = generate_valid_bytes(True, hM0['Q'])
                    hM1['hash'] = md51.hash(bytes)
                    hM1['Q'] = md51.Q
                    hM1['T'] = md51.T
                    hM1['F'] = md51.F
                    hM1['R'] = md51.R
                    hM1['message'] = m1

                    if bitconditions_second_block(hM1['Q']): 
                        m1_prime = [modular_add(m1[i], m1_diff[i]) for i in range(16)]
                        bytes_m1_prime = int_list_to_concatenated_bytes(m1_prime)
                        hM1_prime['hash'] = md51.hash(bytes_m1_prime)
                        hM1_prime['Q'] = md51.Q
                        hM1_prime['T'] = md51.T
                        hM1_prime['F'] = md51.F
                        hM1_prime['R'] = md51.R
                        hM1_prime['message'] = m1_prime

                        second_path_found, step = wang_second_path(hM1, hM1_prime)
                        if second_path_found():
                            print("Success")
                            success_string = "==========================\nM0: " + hM0['message'] + "\nM1: " + hM1['message'] + "\n-----------------------------" +\
                                "\nM0_prime: " + hM0_prime['message'] + "\nM1_prime: " + hM1_prime['message'] + "\n-----------------------------" +\
                                "\n hash(M0): " + hM0['hash'] + "\n hash(M1): " + hM1['hash'] + "\nhash(M0_prime): " + hM0_prime['hash'] + "\nhash(M1_prime): " + hM1_prime['hash']
                            write_to_file('success.txt', success_string)
                            break
                        else:
                            print("Second path failed at step {}".format(step))
                            bytes, message = generate_valid_bytes()
                            hM0 = md51.hash(bytes)
                            Qs = md51.Q
                            break
                
                if second_path_found:
                    break  # break the parent while loop to stop cracking
                    
            else:
                print("First path failed at step {}".format(step))
                bytes, message = generate_valid_bytes()
                hM0 = md51.hash(bytes)
                Qs = md51.Q
        else: # Brute force, god speed
            bytes, message = generate_valid_bytes()
            hM0 = md51.hash(bytes)
            Qs = md51.Q
            
    
    # gui.update_output('Collision found: {}'.format(M1))
    # gui.button_switch()


if __name__ == '__main__':

    from bitarray import bitarray

    # gui.start_app()

    bytes, message = generate_valid_bytes()
    hM0['message'] = message
    hM0['hash'] = md51.hash(bytes)
    hM0['Q'] = md51.Q
    hM0['T'] = md51.T
    hM0['F'] = md51.F
    hM0['R'] = md51.R

    # Start cracking from here:...
    start_cracking(hM0['Q'], message) 
    
