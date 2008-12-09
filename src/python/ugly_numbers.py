NOTHING, PLUS, MINUS = xrange(3)


def ugly(number):
    return any(number % prime == 0 for prime in (2, 3, 5, 7))


for case in xrange(input()):
    digits = list(raw_input())
    result = 0
    for perm in xrange(3 ** (len(digits) - 1)):
        number = 0
        sign = 1
        term = 0
        for pos, digit in enumerate(digits):
            term = term * 10 + int(digit)
            op = (perm // 3 ** pos) % 3
            if op in (PLUS, MINUS):
                number += sign * term
                sign = 1 if op == PLUS else -1
                term = 0
        number += sign * term
        if ugly(number):
            result += 1
    print 'Case #%d: %d' % (case + 1, result)
