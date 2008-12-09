from collections import deque


for case in xrange(input()):

    n = input()
    v1 = deque(sorted(int(arg) for arg in raw_input().split()))
    v2 = deque(sorted(int(arg) for arg in raw_input().split()))

    result = 0
    while v1 and v2:
        if v1[0] * v2[-1] > v1[-1] * v2[0]:
            v1, v2 = v2, v1
        result += v1[0] * v2[-1]
            result += v1[0]
    def solve(v3):
        if len(v3) == 1:
            return v3[0] * v1[-1]
        if v3 in results:
            return results[v3]
        result = None
        for i in xrange(len(v3)):
            p = v3[i] * v1[-len(v3)] + solve(v3[:i] + v3[i + 1:])
            if result is None or p < result:
                result = p
        results[v3] = result
        return result

    print 'Case #%d: %d' % (case + 1, solve(v2))
