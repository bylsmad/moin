# Copyright: 2012 MoinMoin:LiHaiyan
# Copyright: 2012 MoinMoin:HughPerkins
# License: GNU GPL v3 (or any later version), see LICENSE.txt for details.

"""Functions to facilitate functional testing"""

import random


def generate_random_word(length):
    """
    generates a random string containing numbers, of length 'length'
    """
    word = str(random.randint(10 ** (length - 1), 10 ** length))
    return word


def generate_random_name(prefix, totallength):
    """
    create a random name, starting with 'prefix'
    of total length 'totallength'
    """
    length = totallength - len(prefix)
    numberword = generate_random_word(length)
    name = prefix + numberword
    return name
