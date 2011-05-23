import math
import pyximport; pyximport.install()
import detect_rows_fastcore

def get_filled_lines(image, target_color, tolerance):
    res = []
    sq_devs = detect_rows_fastcore.get_sq_dev_per_line(image, target_color)
    thresh = 1.0*image.size[0]*(tolerance**2)
    for sqd in sq_devs:
        res.append(sqd>thresh)
    return res

def get_ranges(image, target_color, tolerance, min_row_ratio, ignore_small_rows=True):

    filled_lines = get_filled_lines(image, target_color, tolerance)
    res = []
    
    start = -1
    min_row_pixels = math.floor(image.size[1]*min_row_ratio)
    for y in xrange(image.size[1]+1):
        filled = (y<image.size[1]) and filled_lines[y]
        if filled:
            if start==-1:
                start = y
        else:
            if start!=-1:
                res.append((start,y))
                start = -1

    
    while len(res)>0 and res[0][1]-res[0][0]<min_row_pixels:
        if ignore_small_rows:
            res = res[1:]
        else:
            res[:2] = [(res[0][0], res[1][1])]
    while len(res)>0 and res[-1][1]-res[-1][0]<min_row_pixels:
        if ignore_small_rows:
            res = res[:-1]
        else:
            res[-2:] = [(res[-2][0], res[-1][1])]

    return res

