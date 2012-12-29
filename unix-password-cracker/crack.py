import argparse
import crypt
import threading

from multiprocessing import Pool


"""
UNIX password cracker
Uses a simple dictionary based brute-force attack to guess a user's
password by hashing the dictionary word and then checking for equality
against the existing hash.  
passwords.txt (as per /etc/passwd)
dictionary.txt (one word per line example file from http://www.math.sjsu.edu/~foster/dictionary.txt)
"""


def test_pass(user, crypt_pass, dict_words):
    salt = crypt_pass[0:2]
    for word in dict_words:
        crypt_word = crypt.crypt(word, salt)
        if crypt_word.strip() == crypt_pass.strip():
            return 'Password for %s is: %s' % (user, word)
            return
    return 'Password for %s not found' % user 

def print_pass(x):
    print x

def use_threading(func, args):
    t = threading.Thread(target=test_pass, args=args)
    t.start()
    return t
    
def use_multithreaded_pools(func, args):
    pool = Pool(processes=10)
    return pool.apply_async(func, args)
    
def main(mode=None):
    dictionary = 'dictionary.txt'
    with open(dictionary, 'r') as f:
        dict_words = [line.strip('\n').strip() for line in f.readlines()]
    
    results = [] # used in 'pool' mode only

    passwords = 'passwords.txt'
    with open(passwords, 'r') as f:
        for line in f.readlines():
            if ":" in line:
                user = line.split(':')[0]
                crypt_pass = line.split(':')[1].strip(' ')
                
                if mode == 'threading':
                    results.append(use_threading(test_pass, [user, crypt_pass, dict_words]))
                elif mode == 'pool':
                    results.append(use_multithreaded_pools(test_pass, [user, crypt_pass, dict_words]))
                else:
                    # default - execute sequentially 
                    results.append(test_pass(user, crypt_pass, dict_words))
        
    if results:     
        for result in results:
            if mode == 'threading':
                pass
            elif mode == 'pool':
                print result.get()
            else:
                print result

if __name__ == "__main__":
    mode = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="increase output verbosity")
    args = parser.parse_args()
    if args.mode:
        mode = args.mode
    main(mode=mode)
