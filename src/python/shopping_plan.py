from collections import defaultdict
from math import sqrt


def main():
    for case in xrange(input()):

        itemcount, storecount, gasprice = (int(arg) for arg
                                           in raw_input().split())

        # Parse items.
        itemargs = raw_input().split()
        itemnames = tuple(arg.rstrip('!') for arg in itemargs)
        perishables = sum(1 << i for i, arg in enumerate(itemargs)
                          if arg.endswith('!'))

        # Parse stores.
        positions = []
        pricelists = []
        inventories = []
        for i in xrange(storecount):
            storeargs = raw_input().split()
            pos = int(storeargs[0]), int(storeargs[1])
            prices = {}
            for pricearg in storeargs[2:]:
                itemname, pricestr = pricearg.split(':')
                price = int(pricestr)
                prices[itemname] = price
            pricelist = [prices.get(itemname, -1) for itemname in itemnames]
            inventory = sum(1 << i for i, itemname in enumerate(itemnames)
                            if itemname in prices)
            positions.append(pos)
            pricelists.append(pricelist)
            inventories.append(inventory)
        positions.append((0, 0))

        def decodeitems(items):
            return (i for i in xrange(itemcount) if items & (1 << i))

        # Precalculate gas costs.
        def gascost(store, dest):
            storex, storey = positions[store]
            destx, desty = positions[dest]
            return gasprice * sqrt((destx - storex) ** 2
                                   + (desty - storey) ** 2)
        stores = range(storecount) + [-1]
        gascosts = [[gascost(store, dest) for dest in stores]
                    for store in stores]

        # Find the minimum cost using memoization.
        mincosts = defaultdict(dict)
        def mincost(store, items, perishing):
            try:
                return mincosts[store, perishing][items]
            except KeyError:
                if not items:

                    # We are done shopping.
                    result = gascosts[store][-1]

                elif perishing:

                    # Return to the house...
                    result = gascosts[store][-1] + mincost(-1, items, False)

                    # ...or buy something more.
                    for i in decodeitems(items & inventories[store]):
                        cost = (pricelists[store][i]
                                + mincost(store, items & ~(1 << i), True))
                        result = min(cost, result)

                else:

                    # Drive to a store and buy something.
                    result = None
                    for dest in xrange(storecount):
                        for i in decodeitems(items & inventories[dest]):
                            cost = (gascosts[store][dest]
                                    + pricelists[dest][i]
                                    + mincost(dest, items & ~(1 << i),
                                              bool(perishables & (1 << i))))
                            if result is None or cost < result:
                                result = cost
                    assert result is not None

                mincosts[store, perishing][items] = result
                return result
        result = mincost(-1, 2 ** itemcount - 1, False)
        print 'Case #%d: %.7f' % (case + 1, result)


if __name__ == '__main__':
    main()
