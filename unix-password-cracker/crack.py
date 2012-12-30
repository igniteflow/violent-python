import argparse
import crypt
import threading

from multiprocessing import Pool, Queue

queue = Queue()

def test_pass(user, crypt_pass, dict_words):
    """Standalone function as multithreading doesn't appear to like instance methods"""
    salt = crypt_pass[0:2]
    for word in dict_words:
        crypt_word = crypt.crypt(word, salt)
        if crypt_word.strip() == crypt_pass.strip():
            queue.put('Password for %s is: %s' % (user, word))
            return
    queue.put('Password for %s not found' % user)


class UnixPasswordCracker(object):
    """
    Uses a simple dictionary based brute-force attack to guess a user's
    password by hashing the dictionary word and then checking for equality
    against the existing hash.  
    passwords.txt (as per /etc/passwd)
    dictionary.txt (one word per line example file from http://www.math.sjsu.edu/~foster/dictionary.txt)
    """
    pool = Pool(processes=5)

    def use_threading(self, func, args):
        t = threading.Thread(target=func, args=args)
        t.start()
        t.join()
        
    def use_multithreaded_pools(self, func, args):
        return self.pool.apply_async(func, args)
        
    def main(self, mode=None):
        dictionary = 'dictionary.txt'
        with open(dictionary, 'r') as f:
            dict_words = [line.strip('\n').strip() for line in f.readlines()]
        
        passwords = 'passwords.txt'
        with open(passwords, 'r') as f:
            for line in f.readlines():
                if ":" in line:
                    user = line.split(':')[0]
                    crypt_pass = line.split(':')[1].strip(' ')
                    args = [user, crypt_pass, dict_words]
                    
                    if mode == 'threading':
                        self.use_threading(test_pass, args)
                    elif mode == 'pool':
                        self.use_multithreaded_pools(test_pass, args)
                    else:
                        test_pass(*args)

        # close the pool and wait for the workers to finish
        self.pool.close()
        self.pool.join()        

        # print the queue items
        while not queue.empty():
            print queue.get()
        

if __name__ == "__main__":
    """
    Performance (from `time` real):
        default (sequential) = 0m8.315s
        threading = 0m8.228s
        pool = 0m6.950s
    @todo These times really should be averages from multiple runs, however they are not, 
    because I am lazy
    """
    mode = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Valid choices: 'pool' and 'threading'")
    args = parser.parse_args()
    if args.mode:
        mode = args.mode
    UnixPasswordCracker().main(mode=mode)
