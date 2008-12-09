for case in xrange(input()):
    search_engines = [raw_input() for i in xrange(input())]
    switches = 0
    unseen = set(search_engines)
    for i in xrange(input()):
        query = raw_input()
        if len(unseen) == 1 and query in unseen:
            switches += 1
            unseen = set(search_engines)
        unseen.discard(query)
    print 'Case #%d: %d' % (case + 1, switches)
