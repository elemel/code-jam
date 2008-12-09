for case in xrange(input()):
    _, key_count, _ = map(int, raw_input().split())
    freqs = sorted(map(int, raw_input().split()))
    total_presses = 0
    for presses in xrange(1, 1000001):
        if not freqs:
            break
        for key in xrange(key_count):
            if not freqs:
                break
            total_presses += presses * freqs.pop()
    print 'Case #%d: %d' % (case + 1, total_presses)

