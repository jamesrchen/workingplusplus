import string
import random

chars = string.ascii_uppercase+"123456789"

def getCode(length=5):
    final = ""
    for i in range(length):
        final += chars[random.randint(0,len(chars)-1)]
    return final