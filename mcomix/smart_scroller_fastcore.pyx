
def count_lines(py_image, py_max_ignore_size, py_want_bg, py_start_step, py_step_size, py_nb_steps, py_line_pitch, py_max_lines):
    cdef:
        const unsigned char *image
        unsigned max_ignore_size
        int want_bg
        unsigned start_step
        int step_size
        unsigned nb_steps
        int line_pitch
        unsigned max_lines
        unsigned count, nb_err, step
        int is_bg
    image = py_image
    max_ignore_size = py_max_ignore_size
    want_bg = 1 if py_want_bg else 0
    start_step = py_start_step
    step_size = py_step_size
    nb_steps = py_nb_steps
    line_pitch = py_line_pitch
    max_lines = py_max_lines
    count = 0
    while count < max_lines:
        is_bg = 1
        nb_err = 0
        for step in range(nb_steps):
            if 0 == image[start_step + step * step_size]:
                nb_err = 0
            else:
                nb_err += 1
                if nb_err > max_ignore_size:
                    is_bg = 0
                    break
        if is_bg != want_bg:
            break
        count += 1
        start_step += line_pitch
    return count

