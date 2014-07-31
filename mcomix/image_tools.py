"""image_tools.py - Various image manipulations."""

import operator

def get_most_common_edge_colour(image, edge=2):
    """Return the most commonly occurring pixel value along the four edges
    of <image>. The return value is a sequence, (r, g, b), with 16 bit
    values.

    Note: This could be done more cleanly with subpixbuf(), but that
    doesn't work as expected together with get_pixels().
    """

    def group_colors(colors, steps=10):
        """ This rounds a list of colors in C{colors} to the next nearest value,
        i.e. 128, 83, 10 becomes 130, 85, 10 with C{steps}=5. This compensates for
        dirty colors where no clear dominating color can be made out.

        @return: The color that appears most often in the prominent group."""

        # Start group
        group = (0, 0, 0)
        # List of (count, color) pairs, group contains most colors
        colors_in_prominent_group = []
        color_count_in_prominent_group = 0
        # List of (count, color) pairs, current color group
        colors_in_group = []
        color_count_in_group = 0

        for count, color in colors:

            # Round color
            rounded = [0] * len(color)
            for i, color_value in enumerate(color):
                if steps % 2 == 0:
                    middle = steps // 2
                else:
                    middle = steps // 2 + 1

                remainder = color_value % steps
                if remainder >= middle:
                    color_value = color_value + (steps - remainder)
                else:
                    color_value = color_value - remainder

                rounded[i] = min(255, max(0, color_value))

            # Change prominent group if necessary
            if rounded == group:
                # Color still fits in the previous color group
                colors_in_group.append((count, color))
                color_count_in_group += count
            else:
                # Color group changed, check if current group has more colors
                # than last group
                if color_count_in_group > color_count_in_prominent_group:
                    colors_in_prominent_group = colors_in_group
                    color_count_in_prominent_group = color_count_in_group

                group = rounded
                colors_in_group = [ (count, color) ]
                color_count_in_group = count

        # Cleanup if only one edge color group was found
        if color_count_in_group > color_count_in_prominent_group:
            colors_in_prominent_group = colors_in_group

        colors_in_prominent_group.sort(key=operator.itemgetter(0), reverse=True)
        # List is now sorted by color count, first color appears most often
        return colors_in_prominent_group[0][1]

    def get_edge_pixbuf(image, side, edge):
        """ Returns a image corresponding to the side passed in <side>.
        Valid sides are 'left', 'right', 'top', 'bottom'. """
        width, height = image.size
        edge = min(edge, width, height)

        if side == 'left':
            box = (0, 0, edge, height)
        elif side == 'right':
            box = (width - edge, 0, width, height)
        elif side == 'top':
            box = (0, 0, width, edge)
        elif side == 'bottom':
            box = (0, height - edge, width, height)
        else:
            assert False, 'Invalid edge side'

        subpix = image.crop(box)

        return subpix

    left_edge = get_edge_pixbuf(image, 'left', edge)
    right_edge = get_edge_pixbuf(image, 'right', edge)

    # Find all edge colors. Color count is separate for all four edges
    ungrouped_colors = []
    for edge in (left_edge, right_edge):
        ungrouped_colors.extend(edge.getcolors(edge.size[0] * edge.size[1]))

    # Sum up colors from all edges
    ungrouped_colors.sort(key=operator.itemgetter(1))
    most_used = group_colors(ungrouped_colors)
    return [color * 257 for color in most_used]

# vim: expandtab:sw=4:ts=4
