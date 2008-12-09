from sys import maxint, stdin

NORTH = -1, 0
SOUTH = 1, 0
WEST = 0, -1
EAST = 0, 1

INIT = 15
BITS = {NORTH: 1, SOUTH: 2, WEST: 4, EAST: 8}
DESCS = '0123456789abcdef'


for casenum in xrange(1, int(stdin.readline()) + 1):

    # Start north of the maze, facing south.
    drow, dcol = SOUTH
    row = col = 0
    prevstep = None

    # Store discovered rooms in a dictionary, with position as key and a bit
    # field of exits as value. Newly discovered rooms have all exit bits set.

    rooms = {}

    # Initialize the maze size.
    minrow = mincol = maxint
    maxrow = maxcol = -maxint - 1

    for path in stdin.readline().split():
        for stepnum, step in enumerate(path):
            if step == 'W' and stepnum and prevstep in 'RW' or step == 'R':

                # There is a wall to the left. Clear the exit bit for it.
                rooms[row, col] &= ~BITS[-dcol, drow]

            if step == 'W':

                # Walk forward.
                row, col = row + drow, col + dcol

                if stepnum != len(path) - 1 and (row, col) not in rooms:

                    # We have entered a new room.
                    rooms[row, col] = INIT

                    # Update the maze size.
                    minrow, mincol = min(row, minrow), min(col, mincol)
                    maxrow, maxcol = max(row, maxrow), max(col, maxcol)

            elif step == 'L':

                # Turn left.
                drow, dcol = -dcol, drow

            elif step == 'R':

                # Turn right.
                drow, dcol = dcol, -drow

            prevstep = step

        # Turn around.
        drow, dcol = -drow, -dcol

    # Print the maze.
    print 'Case #%d:' % casenum
    for row in xrange(minrow, maxrow + 1):
        print ''.join(DESCS[rooms[row, col]]
                      for col in xrange(mincol, maxcol + 1))
