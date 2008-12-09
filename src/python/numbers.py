from decimal import *


setcontext(Context(prec=1000))
d = Decimal(3) + Decimal(5).sqrt()


for case in xrange(input()):
    n = input()
    result = d ** n
    print 'Case #%d: %03d' % (case + 1, int(result % 1000))
