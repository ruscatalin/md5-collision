import gui
import md51
from util import *
from wang import *
import secrets


hM0 = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}
hM0_prime = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}
hM1 = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}
hM1_prime = {'hash': None, 'Q': None, 'T': None, 'F': None, 'R': None, 'message': None}

m0_diff = [0, 0, 0, 0, 2**31, 0, 0, 0, 0, 0, 0, 2**15, 0, 0, 2**31, 0]
m1_diff = [0, 0, 0, 0, 2**31, 0, 0, 0, 0, 0, 0, -2**15, 0, 0, 2**31, 0]


def start_cracking():
    global hM0, hM0_prime, hM1, hM1_prime
    print("Started cracking...")

    while True:
        bytes, message, _ = generate_valid_bytes()
        hM0['message'] = message
        hM0['hash'] = md51.hash(bytes)
        hM0['Q'] = md51.Q
        hM0['T'] = md51.T
        hM0['F'] = md51.F
        hM0['R'] = md51.R
        if secrets.randbelow(10000) <= 4: # 0.04% chance to update
            gui.update_output(''.join([str(m) for m in message]))
            # TODO: maybe write how many hashes per second

        if bitconditions16to64(hM0['Q']): # Check the remaining bitconditions of block1
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
                    bytes, m1, _ = generate_valid_bytes(True, hM0['Q'])
                    hM1['hash'] = md51.hash(bytes)
                    hM1['Q'] = md51.Q
                    hM1['T'] = md51.T
                    hM1['F'] = md51.F
                    hM1['R'] = md51.R
                    hM1['message'] = m1

                    if bitconditions16to64_second_block(hM1['Q']): 
                        m1_prime = [modular_add(m1[i], m1_diff[i]) for i in range(16)]
                        bytes_m1_prime = int_list_to_concatenated_bytes(m1_prime)
                        hM1_prime['hash'] = md51.hash(bytes_m1_prime)
                        hM1_prime['Q'] = md51.Q
                        hM1_prime['T'] = md51.T
                        hM1_prime['F'] = md51.F
                        hM1_prime['R'] = md51.R
                        hM1_prime['message'] = m1_prime

                        second_path_found, step = wang_second_path(hM1, hM1_prime)
                        if second_path_found:
                            print("Success")
                            success_string = "==========================\nM0: " + hM0['message'] + "\nM1: " + hM1['message'] + "\n-----------------------------" +\
                                "\nM0_prime: " + hM0_prime['message'] + "\nM1_prime: " + hM1_prime['message'] + "\n-----------------------------" +\
                                "\n hash(M0): " + hM0['hash'] + "\n hash(M1): " + hM1['hash'] + "\nhash(M0_prime): " + hM0_prime['hash'] + "\nhash(M1_prime): " + hM1_prime['hash']
                            write_to_file('success.txt', success_string)
                            break
                        else:
                            print("Second path failed at step {}".format(step))
                            break
                if second_path_found:
                    break  # break the parent while loop to stop cracking   
            else:
                print("First path failed at step {}".format(step))

    gui.update_output('Collision found!\nCheck success.txt')
    gui.button_switch()



def start_cracking_step_by_step():

    print("Started cracking step by step...")
    while True:
        bytes, message, hM0['Q'] = generate_valid_bytes()
        hM0['message'] = message

        if secrets.randbelow(10000) <= 4: # 0.04% chance to update
            gui.update_output(''.join([str(m) for m in message]))

        md51.message = bytes
        md51.Q = hM0['Q']
        all_good = False
        # Check the remaining 16-64 bitconditions
        for i in range(16, 64):
            md51.md5_one_step(i)
            if bitconditions16to64(md51.Q, exact_step=i):
                hM0['Q'].append(md51.Q[-1])
                if i == 64:
                    all_good = True
                continue
            else:
                md51.Q, md51.T, md51.F, md51.R = None, None, None, None
                break
        if not all_good:
            continue
        else:
            write_to_file('log.txt', '\n 16-64: ' + ''.join([str(m) for m in message]))




if __name__ == '__main__':
    message = None    
    gui.start_app()

    
