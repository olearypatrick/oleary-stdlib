"""
stdrandom.py

The stdrandom module defines functions related to pseudo-random numbers.
"""

# ----------------------------------------------------------------------------------------------------------------------

import random
import math


# ----------------------------------------------------------------------------------------------------------------------

def seed(i=None):
    """
    Seed the random number generator as hash(i), where i is an int. If i is None, then seed using the current time or,
    quoting the help page for random.seed(), "an operating system specific randomness source if available."
    """
    random.seed(i)


# ----------------------------------------------------------------------------------------------------------------------

def uniform_int(lo, hi):
    """
    Return an integer chosen uniformly from the range [lo, hi).
    """
    return random.randrange(lo, hi)


# ----------------------------------------------------------------------------------------------------------------------

def uniform_float(lo, hi):
    """
    Return a number chosen uniformly from the range [lo, hi).
    """
    return random.uniform(lo, hi)


# ----------------------------------------------------------------------------------------------------------------------

def bernoulli(p=0.5):
    """
    Return True with probability p.
    """
    return random.random() < p

# ----------------------------------------------------------------------------------------------------------------------


def binomial(n, p=0.5):
    """
    Return the number of heads in n coin flips, each of which is heads with probability p.
    """
    heads = 0
    for i in range(n):
        if bernoulli(p):
            heads += 1
    return heads


# ----------------------------------------------------------------------------------------------------------------------

def gaussian(mean=0.0, stddev=1.0):
    """
    Return a float according to a standard Gaussian distribution with the given mean (mean) and standard deviation
    (stddev).
    """
    return random.gauss(mean, stddev)


# ----------------------------------------------------------------------------------------------------------------------

def discrete(a):
    """
    Return a float from a discrete distribution: i with probability a[i].  Precondition: the elements of array a sum to
    1.
    """
    r = uniform_float(0.0, sum(a))
    subtotal = 0.0
    for i in range(len(a)):
        subtotal += a[i]
        if subtotal > r:
            return i


# ----------------------------------------------------------------------------------------------------------------------

def shuffle(a):
    """
    Shuffle array a.
    """
    random.shuffle(a)


# ----------------------------------------------------------------------------------------------------------------------

def exp(lambd):
    """
    Return a float from an exponential distribution with rate lambd.
    """
    return -math.log(1 - random.random()) / lambd


# ----------------------------------------------------------------------------------------------------------------------

def _main():
    """
    For testing.
    """
    import sys
    import stdio
    seed(1)
    n = int(sys.argv[1])
    for i in range(n):
        stdio.writef(' %2d ', uniform_int(10, 100))
        stdio.writef('%8.5f ', uniform_float(10.0, 99.0))
        stdio.writef('%5s ', bernoulli())
        stdio.writef('%5s ', binomial(100, .5))
        stdio.writef('%7.5f ', gaussian(9.0, .2))
        stdio.writef('%2d ', discrete([.5, .3, .1, .1]))
        stdio.writeln()


if __name__ == '__main__':
    _main()
