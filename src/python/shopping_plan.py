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
    item_count, store_count, gas_price = (int(arg) for arg
                                          in raw_input().split())
    item_names, perishables = parse_items()
    stores = parse_stores(store_count)
    return gas_price, item_names, perishables, stores

def parse_items():    
    item_args = raw_input().split()
    item_names = [arg.rstrip('!') for arg in item_args]
    perishables = [arg.rstrip('!') for arg in item_args if arg.endswith('!')]
    return item_names, perishables

def parse_stores(store_count):
    stores = {}
    for _ in xrange(store_count):
        store_args = raw_input().split()
        pos = int(store_args[0]), int(store_args[1])
        prices = {}
        for price_arg in store_args[2:]:
            item_name, price = price_arg.split(':')
            prices[item_name] = int(price)
        stores[pos] = prices
    return stores

def solve(gas_price, item_names, perishables, stores):
    def decode_items(items):
        return (i for i in xrange(len(item_names)) if items & (1 << i))

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
        return item_names[i] in perishables

    @memoize
    def min_cost(pos, items, perishing):
        if not items:

            # We are done shopping.
            return gas_cost(pos, (0, 0))

        elif perishing:

            # Return to the house...
            result = gas_cost(pos, (0, 0)) + min_cost((0, 0), items, False)

            # ...or buy something more.
            for i in decode_items(items & inventory(pos)):
                cost = (item_cost(pos, i) +
                        min_cost(pos, items & ~(1 << i), True))
                result = min(cost, result)
            return result

        else:

            # Drive to a store and buy something.
            result = float('inf')
            for dest in stores:
                for i in decode_items(items & inventory(dest)):
                    cost = (gas_cost(pos, dest) + item_cost(dest, i) +
                            min_cost(dest, items & ~(1 << i), perishable(i)))
                    result = min(cost, result)
            return result
    return min_cost((0, 0), (1 << len(item_names)) - 1, False)

def main():
    for case in xrange(input()):
        gas_price, item_names, perishables, stores = parse()
        result = solve(gas_price, item_names, perishables, stores)
        print 'Case #%d: %.7f' % (case + 1, result)

if __name__ == '__main__':
    main()
