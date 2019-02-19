from cryptography.fernet import Fernet


""" key = Fernet.generate_key()

loginFOpen = open("login.bin", "wb")
loginFOpen.write(key)
loginFOpen.close() """

loginFRetrieve = open("LK.bin", "r")

retrivedKey =  loginFRetrieve.read()
print(retrivedKey)
cipher_suite = Fernet(retrivedKey)
loginFRetrieve.close()

cipher_text = cipher_suite.encrypt(b"localhost root root logindatabase")

writeLC = open("LC.bin", "rb")
retrieve = writeLC.read()
print(cipher_suite.decrypt(retrieve))