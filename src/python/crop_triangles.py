def generate_trees(n, a, b, c, d, x0, y0, m):
    x, y = x0, y0
    yield x, y
    for i in xrange(1, n):
        x = (a * x + b) % m
        y = (c * y + d) % m
        yield x, y


def valid_triangle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (x1 + x2 + x3) % 3 == 0 and (y1 + y2 + y3) % 3 == 0


for case in xrange(input()):

    args = map(int, raw_input().split())
    trees = list(generate_trees(*args))

    result = 0
    for i1 in xrange(len(trees) - 2):
        for i2 in xrange(i1 + 1, len(trees) - 1):
            for i3 in xrange(i2 + 1, len(trees)):
                if valid_triangle(trees[i1], trees[i2], trees[i3]):
                    result += 1

    print 'Case #%d: %d' % (case + 1, result)
