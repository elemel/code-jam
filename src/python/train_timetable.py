def parse_time(arg):
    hours, minutes = map(int, arg.split(':'))
    return hours * 60 + minutes


for case in xrange(input()):

    # Parse input.
    turnaround_time = input()
    a_count, b_count = map(int, raw_input().split())
    trips = []
    for i in xrange(a_count + b_count):
        origin, destination = 'AB' if i < a_count else 'BA'
        departure, arrival = map(parse_time, raw_input().split())
        trips.append((origin, destination, departure, arrival))

    # Initialize state.
    trains = {'A': 0, 'B': 0}
    min_trains = dict(trains)

    # Define event handlers.
    def depart(station):
        trains[station] -= 1
        min_trains[station] = min(trains[station], min_trains[station])
    def arrive(station):
        trains[station] += 1

    # Create a stack of events. The turnaround time is simply added to the
    # arrival time. We also use a tiebreaker to ensure that arrivals are
    # handled before departures occuring at the same time.

    events = []
    for origin, destination, departure, arrival in trips:
        events.append((departure, 1, depart, origin))
        events.append((arrival + turnaround_time, 0, arrive, destination))
    events.sort(reverse=True)

    # Pop events.
    while events:
        time, tiebreaker, event_handler, station = events.pop()
        event_handler(station)

    # Print result.
    print 'Case #%d: %d %d' % (case + 1, -min_trains['A'], -min_trains['B'])
