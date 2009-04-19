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
    _, store_count, gas_price = (int(s) for s in raw_input().split())
    return gas_price, parse_items(), parse_stores(store_count)

def parse_items():    
    return dict((s.rstrip('!'), s.endswith('!')) for s in raw_input().split())

def parse_stores(store_count):
    return dict(parse_store() for _ in xrange(store_count))

def parse_store():
    store_args = raw_input().split()
    pos = int(store_args[0]), int(store_args[1])
    prices = {}
    for price_arg in store_args[2:]:
        item_name, price = price_arg.split(':')
        prices[item_name] = int(price)
    return pos, prices

def solve(gas_price, items, stores):
    item_names = sorted(items)

    @memoize
    def bits(mask):
        return [i for i in xrange(len(item_names)) if mask & (1 << i)]

    @memoize
    def gas_cost(pos, dest):
        pos_x, pos_y = pos
        dest_x, dest_y = dest
        return gas_price * sqrt((dest_x - pos_x) ** 2
                                + (dest_y - pos_y) ** 2)

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
    def min_cost(pos, mask, perishing):
        if not mask:

            # We are done shopping.
            return gas_cost(pos, (0, 0))

        elif perishing:

            # Return to the house...
            result = gas_cost(pos, (0, 0)) + min_cost((0, 0), mask, False)

            # ...or buy something more.
            for i in bits(mask & inventory(pos)):
                cost = (item_cost(pos, i) +
                        min_cost(pos, mask & ~(1 << i), True))
                result = min(cost, result)
            return result

        else:

            # Drive to a store and buy something.
            result = float('inf')
            for dest in stores:
                for i in bits(mask & inventory(dest)):
                    cost = (gas_cost(pos, dest) + item_cost(dest, i) +
                            min_cost(dest, mask & ~(1 << i), perishable(i)))
                    result = min(cost, result)
            return result
    return min_cost((0, 0), (1 << len(item_names)) - 1, False)

def main():
    for case in xrange(input()):
        gas_price, items, stores = parse()
        result = solve(gas_price, items, stores)
        print 'Case #%d: %.7f' % (case + 1, result)

if __name__ == '__main__':
    main()
