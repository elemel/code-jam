from math import acos, pi, sqrt
from sys import maxint


# Calculate the area of a circle segment inscribed in a rectangle.
def segment_area(left, bottom, right, top, radius):
    x = sqrt(((left + right) / 2) ** 2 + ((bottom + top) / 2) ** 2)
    y = sqrt(radius ** 2 - x ** 2)
    angle = acos(x / radius)
    return angle * radius ** 2 - x * y


def hole_area(left, bottom, right, top, radius):

    # Determine the intersection points for the circle and the square.
    if radius ** 2 <= left ** 2 + top ** 2:
        left_cut = sqrt(radius ** 2 - left ** 2)
        top_cut = None
    else:
        left_cut = None
        top_cut = sqrt(radius ** 2 - top ** 2)
    if radius ** 2 <= right ** 2 + bottom ** 2:
        right_cut = None
        bottom_cut = sqrt(radius ** 2 - bottom ** 2)
    else:
        right_cut = sqrt(radius ** 2 - right ** 2)
        bottom_cut = None

    # Handle the four different cases.
    if left_cut is not None and bottom_cut is not None:

        # The circle intersects the left side and the bottom side. We divide
        # the intersection into a triangle and a circle segment.

        return ((bottom_cut - left) * (left_cut - bottom) / 2
                + segment_area(left, bottom, bottom_cut, left_cut, radius))

    elif left_cut is not None and right_cut is not None:

        # The circle intersects the left side and the right side. We divide the
        # intersection into a rectangle, a triangle, and a circle segment.

        return ((right - left) * (right_cut - bottom)
                + (right - left) * (left_cut - right_cut) / 2
                + segment_area(left, right_cut, right, left_cut, radius))

    elif top_cut is not None and bottom_cut is not None:

        # The circle intersects the top side and the bottom side. This case
        # mirrors the one above.

        return ((top_cut - left) * (top - bottom)
                + (bottom_cut - top_cut) * (top - bottom) / 2
                + segment_area(top_cut, bottom, bottom_cut, top, radius))

    else:

        # The circle intersects the top side and the right side. We divide the
        # intersection into a square, a negative triangle, and a circle
        # segment.

        return ((right - left) * (top - bottom)
                - (right - top_cut) * (top - right_cut) / 2
                + segment_area(top_cut, right_cut, right, top, radius))


for case in xrange(input()):

    # Parse input.
    fly_radius, outer_radius, thickness, string_radius, gap \
        = map(float, raw_input().split())

    # Simplification 1: The problem is equivalent to one where
    #
    #   fly_radius' = 0,
    #   thickness' = thickness + fly_radius
    #   string_radius' = string_radius + fly_radius
    #   gap' = gap - 2 * fly_radius

    thickness += fly_radius
    string_radius += fly_radius
    gap -= 2 * fly_radius

    if gap <= 0:
        probability = 1.0
    else:

        # Simplification 2: Because of symmetry, we can consider the whole
        # tennis racquet, half of it, a quadrant, or an octant. We choose the
        # top right quadrant.

        inner_radius = outer_radius - thickness
        step = gap + 2 * string_radius
        miss_area = 0.0
        for column in xrange(maxint):
            left = step * column + string_radius
            if left >= inner_radius:
                break
            for row in xrange(maxint):
                bottom = step * row + string_radius
                if left ** 2 + bottom ** 2 >= inner_radius ** 2:
                    break
                right, top = left + gap, bottom + gap
                if right ** 2 + top ** 2 <= inner_radius ** 2:
                    miss_area += gap ** 2
                else:
                    miss_area += hole_area(left, bottom, right, top,
                                           inner_radius)
        fly_area = pi * outer_radius ** 2 / 4
        probability = 1.0 - miss_area / fly_area

    # Print result.
    print 'Case #%d: %.6f' % (case + 1, probability)
