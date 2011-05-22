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

def get_ranges(image, target_color, tolerance, min_row_ratio):

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
                if y-start>min_row_pixels:
                    res.append((start,y))
                    start = -1
    return res

