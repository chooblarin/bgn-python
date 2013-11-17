# -*- coding: utf-8 -*-

from random import randint
from itertools import product

LENGTH = 3

def create_answr(s=None):
    s = s or set()
    if len(s) >= LENGTH: return list(s)
    s.add(randint(0,9))
    return create_answr(s)

def get_input_num(): 
    in_num = raw_input('Input your number: ')
    msg = validate_num(in_num.strip())
    if msg:
        print msg
        return get_input_num()
    else:
        return [int(x) for x in list(in_num)]

def validate_num(num):
    if not num.isdigit():
        return 'Digit Error.'
    if len(num) != LENGTH:
        return 'Length Error.'
    if len(set(num)) < LENGTH:
        return 'Duplication Error.'
    return ''

def judge(answr, guess):
    r1 = [x[0] == x[1] for x in zip(answr, guess)]
    r2 = [x[0] == x[1] for x in list(product(answr, guess))]
    hit = r1.count(True)
    blow = r2.count(True) - hit
    return hit, blow

def game(answr, guess, turn):
    result = judge(answr, guess)
    print "turn: %d" % turn
    if answr == guess: 
        print "Congrats!"
    else: 
        print "hit: %d, blow: %d" % result        
        game(answr, get_input_num(), turn + 1)

if __name__ == '__main__':
    answr = create_answr()
    guess = get_input_num()
    game(answr, guess, 1)
