from sys import stdin

for case_num in xrange(1, int(stdin.readline()) + 1):
    alien_num, source_lang, target_lang = stdin.readline().split()
    source_dict = dict((digit, pos) for pos, digit in enumerate(source_lang))
    num = sum(source_dict[digit] * len(source_lang) ** pos
              for pos, digit in enumerate(reversed(alien_num)))
    target_num = []
    while num:
        num, digit = divmod(num, len(target_lang))
        target_num.append(target_lang[digit])
    print 'Case #%d: %s' % (case_num, ''.join(reversed(target_num)))
