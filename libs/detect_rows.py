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
                res.append((start,y))
                start = -1

    small_rows_found = True
    while small_rows_found:
        small_rows_found = False
        for i,r in enumerate(res):
            if r[1]-r[0]<min_row_pixels:
                prev_row = 999999 if i==0 else res[i-1][1]-res[i-1][0]
                next_row = 999999 if i==len(res)-1 else res[i+1][1]-res[i+1][0]
                if prev_row == next_row == 999999:
                    break
                small_rows_found = True
                if prev_row<next_row:
                    res[i-1:i+1] = [(res[i-1][0], res[i][1])]
                if prev_row>next_row:
                    res[i:i+2] = [(res[i][0], res[i+1][1])]
                
    return res

