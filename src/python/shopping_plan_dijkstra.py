from heapq import heappop, heappush
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

def dijkstra(start, goal, neighbors, cost):
    parents = {start: None}
    costs = {start: 0}
    visited = set()
    heap = [(0, start)]
    while heap:
        vertex_cost, vertex = heappop(heap)
        if vertex in visited:
            continue
        visited.add(vertex)
        if goal(vertex):
            return vertex, parents, costs
        for neighbor in neighbors(vertex):
            if neighbor not in visited:
                neighbor_cost = vertex_cost + cost(vertex, neighbor)
                if neighbor not in costs or neighbor_cost < costs[neighbor]:
                    parents[neighbor] = vertex
                    costs[neighbor] = neighbor_cost
                    heappush(heap, (neighbor_cost, neighbor))
    return None, parents, costs

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
    def item_cost(pos, mask):
        return sum(stores[pos][item_names[i]] for i in bits(mask))

    @memoize
    def perishable(i):
        return items[item_names[i]]

    def goal(vertex):
        pos, remaining, _ = vertex
        return pos == home and not remaining

    def neighbors(vertex):
        pos, remaining, perishing = vertex
        if perishing or not remaining:
            yield home, remaining, False
        if not perishing:
            for dest in stores:
                yield dest, remaining, False
        if pos != home:
            for i in bits(remaining & inventory(pos)):
                yield pos, remaining & ~(1 << i), perishing or perishable(i)

    def cost(vertex_a, vertex_b):
        pos_a, remaining_a, _ = vertex_a
        pos_b, remaining_b, _ = vertex_b
        return (gas_cost(pos_a, pos_b) +
                item_cost(pos_b, remaining_a ^ remaining_b))

    start = home, (1 << len(item_names)) - 1, False
    vertex, parents, costs = dijkstra(start, goal, neighbors, cost)
    return costs[vertex]

def main():
    for case in xrange(input()):
        gas_price, items, stores = parse()
        result = solve(gas_price, items, stores)
        print 'Case #%d: %.7f' % (case + 1, result)

if __name__ == '__main__':
    main()
