# -*- coding: utf-8 -*-
import string
import random


def gen_random_str(length,
                   digits=True,
                   ascii_lowercase=True,
                   ascii_uppercase=False):
    chars = ''
    if digits:
        chars += string.digits
    if ascii_lowercase:
        chars += string.ascii_lowercase
    if ascii_uppercase:
        chars += string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(length))
