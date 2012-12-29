import crypt
import threading

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
			print 'Password for %s is: %s \n' % (user, word)
			return
	print 'Password for %s not found \n' % user 

def main():
	dictionary = 'dictionary.txt'
	with open(dictionary, 'r') as f:
		dict_words = [line.strip('\n').strip() for line in f.readlines()]
	
	passwords = 'passwords.txt'
	with open(passwords, 'r') as f:
		for line in f.readlines():
			if ":" in line:
				user = line.split(':')[0]
				crypt_pass = line.split(':')[1].strip(' ')
				t = threading.Thread(target=test_pass, args=[user, crypt_pass, dict_words])
				t.start()
			
if __name__ == "__main__":
	main()