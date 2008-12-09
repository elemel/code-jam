from collections import deque


def validate(deck, start=1):
    deck = list(deck)
    for card in xrange(start, start + len(deck)):
        j = (card - 1) % len(deck)
        if deck[j] != card:
            return False
        deck = deck[j + 1:] + deck[:j]
    return True


for case in xrange(input()):

    k = input()
    args = raw_input().split()
    n = int(args[0])
    indices = map(int, args[1:])

    deck = deque()
    for card in xrange(k, 0, -1):
        deck.appendleft(card)
        deck.rotate(card - 1)
        # assert validate(deck, card)
    # assert validate(deck)
        
    result = ' '.join(str(deck[i - 1]) for i in indices)
    print 'Case #%d: %s' % (case + 1, result)
