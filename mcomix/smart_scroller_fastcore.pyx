
def is_bg_line(image, max_ignore_size, start, end, step):
    cdef:
        unsigned char *s
        unsigned char max_err
        unsigned int start_pos, pos_inc, end_pos, pos
        unsigned char count
        unsigned char pix
    s = image
    max_err = max_ignore_size
    start_pos = start
    pos_inc = step
    end_pos = end
    count = 0
    for pos in range(start_pos, end_pos + pos_inc, pos_inc):
        pix = s[pos]
        if 0 == pix:
            count = 0
        else:
            count += 1
            if count > max_err:
                return False
    return True

