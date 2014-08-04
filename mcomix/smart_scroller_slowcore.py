
def count_lines(image, max_ignore_size, want_bg, start_step, step_size, nb_steps, line_pitch, max_lines):
    count = 0
    while count < max_lines:
        is_bg = True
        nb_err = 0
        for step in range(nb_steps):
            if 0 == image[start_step + step * step_size]:
                nb_err = 0
            else:
                nb_err += 1
                if nb_err > max_ignore_size:
                    is_bg = False
                    break
        if is_bg != want_bg:
            break
        count += 1
        start_step += line_pitch
    return count

