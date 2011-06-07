import math
try:
    import detect_rows_fastcore
except ImportError:
    import pyximport; pyximport.install()
    import detect_rows_fastcore

def get_filled_lines(image, target_color, tolerance):
    res = []
    sq_devs = detect_rows_fastcore.get_sq_dev_per_line(image, target_color)
    thresh = 1.0*image.size[0]*(tolerance**2)
    for sqd in sq_devs:
        res.append(sqd>thresh)
    return res

# each resulting range is: [start, end, scrollable]
# scrollable is a hint to displayer, whether it's worth to try to fit the whole row on screen

def get_ranges(image, target_color, tolerance, min_row_ratio, ignore_small_rows=True):

    filled_lines = get_filled_lines(image, target_color, tolerance)
    ranges = []
    
    start = -1
    min_row_pixels = int(math.floor(image.size[1]*min_row_ratio))
    for y in xrange(image.size[1]+1):
        filled = (y<image.size[1]) and filled_lines[y]
        if filled:
            if start==-1:
                start = y
        else:
            if start!=-1:
                ranges.append((start,y))
                start = -1

    def is_small(r):
        return r[1]-r[0]<min_row_pixels

    # dealing with small ranges
    res = []
    smalls = []
    for r in ranges+[None]:
        if r==None or not is_small(r):
            if smalls:
                coerced = (smalls[0][0], smalls[-1][1], True)
                if (not is_small(coerced)) or (not ignore_small_rows):
                    res.append(coerced)
                smalls = []
            if r!=None:
                res.append((r[0], r[1], False))
        else:
            smalls.append(r)

    
    if len(res)==0:
        return [(0,image.size[1], True)]

    return res


