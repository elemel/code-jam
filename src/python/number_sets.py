from sys import maxint


def sieve(stop=maxint):
    primes = []
    for i in xrange(1, stop):
        for prime in primes:
            if prime != 1 and i % prime == 0:
                break
        else:
            yield i
            primes.append(i)


def factorize(i, primes):
    for prime in primes:
        if prime > i:
            break
        while prime != 1 and i % prime == 0:
            yield prime
            i //= prime


def merge(sets, i, j):
    target = sets[i]
    source = sets[j]
    while source:
        k = source.pop()
        target.add(k)
        sets[k] = target


for case in xrange(input()):

    a, b, p = map(int, raw_input().split())

    sets = dict((i, set([i])) for i in xrange(a, b + 1))
    primes = list(sieve(max(a, b) + 1))
    factors = dict((i, set(factorize(i, primes))) for i in xrange(a, b + 1))

    merges = 0
    for i in xrange(a, b):
        for j in xrange(i + 1, b + 1):
            if (sets[i] is not sets[j]
                and any(factor >= p for factor in factors[i] & factors[j])):
                merge(sets, i, j)
                merges += 1
            
    print 'Case #%d: %d' % (case + 1, len(sets) - merges)
