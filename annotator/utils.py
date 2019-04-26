
import random

seed = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def random_generate_string(len=15):
    ret = []
    for i in range(len):
        ret.append(random.choice(seed))
    return ''.join(ret)

if __name__ == '__main__':
    s = random_generate_string(8)
    print(s)