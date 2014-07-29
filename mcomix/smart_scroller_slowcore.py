#!/usr/bin/env python

def is_bg_line(image, max_ignore_size, pos, end, step):
    count = 0
    while pos < end:
        if 0 == image[pos]:
            count = 0
        else:
            count += 1
            if count > max_ignore_size:
                return False
        pos += step
    return True

