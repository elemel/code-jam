from collections import defaultdict
from math import sqrt

def memoize(func):
    results = {}
    def wrapper(*args):
        try:
            return results[args]
        except KeyError:
            results[args] = func(*args)
            return results[args]
    return wrapper

def parse():
    _, store_count, gas_price = (int(arg) for arg in raw_input().split())
    return gas_price, parse_items(), parse_stores(store_count)

def parse_items():
    return dict((arg.rstrip('!'), arg.endswith('!'))
                for arg in raw_input().split())

def parse_stores(store_count):
    return dict(parse_store() for _ in xrange(store_count))

def parse_store():
    args = raw_input().split()
    pos = int(args[0]), int(args[1])
    prices = dict(parse_price(arg) for arg in args[2:])
    return pos, prices

def parse_price(arg):
    item_name, price = arg.split(':')
    return item_name, int(price)

def solve(gas_price, items, stores):
    home = 0, 0
    item_names = sorted(items)

    @memoize
    def bits(mask):
        return [i for i in xrange(len(item_names)) if mask & (1 << i)]

    @memoize
    def gas_cost(pos, dest):
        pos_x, pos_y = pos
        dest_x, dest_y = dest
        return gas_price * sqrt((dest_x - pos_x) ** 2 +
                                (dest_y - pos_y) ** 2)

    @memoize
    def inventory(pos):
        return sum(1 << i for i, name in enumerate(item_names)
                   if name in stores[pos])

    @memoize
    def item_cost(pos, i):
        return stores[pos][item_names[i]]

    @memoize
    def perishable(i):
        return items[item_names[i]]

    @memoize
    def min_cost(pos, remaining, perishing):
        if not remaining:
            return gas_cost(pos, home)
        elif perishing:
            return min(drop(pos, remaining), buy_more(pos, remaining))
        else:
            return drive_and_buy(pos, remaining)

    def drop(pos, remaining):
        return gas_cost(pos, home) + min_cost(home, remaining, False)

    def buy_more(pos, remaining):
        result = float('inf')
        for i in bits(remaining & inventory(pos)):
            cost = (item_cost(pos, i) +
                    min_cost(pos, remaining & ~(1 << i), True))
            result = min(cost, result)
        return result

    def drive_and_buy(pos, remaining):
        result = float('inf')
        for dest in stores:
            for i in bits(remaining & inventory(dest)):
                cost = (gas_cost(pos, dest) + item_cost(dest, i) +
                        min_cost(dest, remaining & ~(1 << i), perishable(i)))
                result = min(cost, result)
        return result

    return min_cost(home, (1 << len(item_names)) - 1, False)

def main():
    for case in xrange(input()):
        gas_price, items, stores = parse()
        result = solve(gas_price, items, stores)
        print 'Case #%d: %.7f' % (case + 1, result)

if __name__ == '__main__':
    main()
