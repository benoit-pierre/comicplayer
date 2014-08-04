
from mcomix import image_tools
from mcomix import log

from collections import namedtuple

_using_fastcore = True

try:
    from mcomix.smart_scroller_pyrex import *
except ImportError:
    try:
        import pyximport; pyximport.install()
        from mcomix.smart_scroller_fastcore import *
    except ImportError:
        log.warning('Not using smart_scroller_fastcore!')
        from mcomix.smart_scroller_slowcore import *
        _using_fastcore = False

Rect = namedtuple('Rect', 'x y w h')
Rect.__repr__ = lambda r: '%+d%+d:%ux%u' % (r.x, r.y, r.w, r.h)
Rect.x0 = property(lambda r: r.x)
Rect.y0 = property(lambda r: r.y)
Rect.x1 = property(lambda r: r.x + r.w - 1)
Rect.y1 = property(lambda r: r.y + r.h - 1)
Rect.points = property(lambda r: (r.x0, r.y0, r.x1, r.y1))
Rect.from_points = classmethod(lambda cls, x0, y0, x1, y1: cls(x0, y0, x1 - x0 + 1, y1 - y0 + 1))

Frame = namedtuple('Frame', 'rect number split')
Frame.__repr__ = lambda f: '%u%s:%s' % (f.number, '' if f.split is None else '.%u' % f.split, f.rect)

class SmartScroller(object):

    def __init__(self, debug=False):
        self._debug = debug
        self._max_imperfection_size = 3
        self._luminance_threshold = 16
        self._frames = []
        # First/last visible frames.
        self._current_frames = (0, 0)
        self._smart_scroll_possible = False
        self._image_width = 0
        self._image_height = 0
        self._view_x = 0
        self._view_y = 0
        self._view_width = 0
        self._view_height = 0

    def _count_lines(self, bg, start_step, step_size, nb_steps, start_line, line_pitch, max_lines):
        pos = start_step * step_size + start_line * line_pitch
        return count_lines(self._image, self._max_imperfection_size, bg, pos,
                           step_size, nb_steps, line_pitch, max_lines)

    def _crop_side(self, rect, side):
        x0, y0, x1, y1 = rect.points
        if   'top' == side:
            y0 += self._count_lines(True, x0, 1, rect.w, y0, +self._image_width, rect.h)
        elif 'bottom' == side:
            y1 -= self._count_lines(True, x0, 1, rect.w, -y1, -self._image_width, rect.h)
        elif 'left' == side:
            x0 += self._count_lines(True, y0, +self._image_width, rect.h, x0, +1, rect.w)
        elif 'right' == side:
            x1 -= self._count_lines(True, y0, +self._image_width, rect.h, -x1, -1, rect.w)
        else:
            raise ValueError('invalid side argument: %s' % side)
        return Rect.from_points(x0, y0, x1, y1)

    def _crop(self, rect):
        for side in ('top', 'bottom', 'left', 'right'):
            rect = self._crop_side(rect, side)
            if 0 == rect.w or 0 == rect.h:
                return None
        return rect

    def _find_frames(self, rect, split_horz=True, split_vert=True):
        rect = self._crop(rect)
        if rect is None:
            # Empty.
            return None
        if rect.w < self._min_frame_width or rect.h < self._min_frame_height:
            # Too small.
            return None
        for split, horizontal in ((split_horz, True), (split_vert, False)):
            if not split:
                continue
            if horizontal:
                min_nb_lines = self._min_frame_height
                start_step, step_size, nb_steps = rect.x, 1, rect.w
                start_line, line_pitch, nb_lines = rect.y, self._image_width, rect.h
                first_split = lambda: (rect.x, rect.y, rect.w, split_size)
                second_split = lambda: (rect.x, split.y + split.h, rect.w, rect.h - split.h)
            else:
                min_nb_lines = self._min_frame_width
                start_step, step_size, nb_steps = rect.y, self._image_width, rect.h
                start_line, line_pitch, nb_lines = rect.x, 1, rect.w
                first_split = lambda: (rect.x, rect.y, split_size, rect.h)
                second_split = lambda: (split.x + split.w, rect.y, rect.w - split.w, rect.h)
            if nb_lines <= min_nb_lines * 2:
                return None
            cur_line = start_line + min_nb_lines
            end_line = cur_line + nb_lines - 2 * min_nb_lines
            while cur_line < end_line:
                nb_fg_lines = self._count_lines(False, start_step, step_size, nb_steps,
                                                cur_line, line_pitch, end_line - cur_line)
                split_size = cur_line + nb_fg_lines - start_line + 1
                split = Rect(*first_split())
                first_frames = self._find_frames(split,
                                                 split_horz=not horizontal,
                                                 split_vert=horizontal)
                if first_frames is None:
                    cur_line += nb_fg_lines
                    if cur_line >= end_line:
                        break
                    # Skip blank.
                    nb_bg_lines = self._count_lines(True, start_step, step_size, nb_steps,
                                                    cur_line, line_pitch, end_line - cur_line)
                    cur_line += nb_bg_lines
                    continue
                split = Rect(*second_split())
                second_frames = self._find_frames(split)
                if second_frames is None:
                    break
                return first_frames + second_frames
        return [rect]

    def _is_rect_inside(self, rect, bbox):
        if rect.x < bbox.x:
            return False
        if rect.y < bbox.y:
            return False
        if rect.x + rect.w > bbox.x + bbox.w:
            return False
        if rect.y + rect.h > bbox.y + bbox.h:
            return False
        return True

    def _grow_bbox(self, bbox, rect):
        x = min(bbox.x, rect.x)
        y = min(bbox.y, rect.y)
        w = max(bbox.x + bbox.w, rect.x + rect.w)
        h = max(bbox.y + bbox.h, rect.y + rect.h)
        return Rect(x, y, w - x, h - y)

    def _split_frame(self, frame, max_width, max_height):
        if frame.rect.w <= max_width and frame.rect.h <= max_height:
            return (frame,)
        splits = []
        if frame.rect.h <= max_height:
            nb_horz_splits = 1
            split_height = frame.rect.h
        else:
            nb_horz_splits = (frame.rect.h + max_height - 1) / max_height
            split_height = frame.rect.h / nb_horz_splits
        if frame.rect.w <= max_width:
            nb_vert_splits = 1
            split_width = frame.rect.w
        else:
            nb_vert_splits = (frame.rect.w + max_width - 1) / max_width
            split_width = frame.rect.w / nb_vert_splits
        splits = []
        y = frame.rect.y
        for _ in range(nb_horz_splits):
            x = frame.rect.x
            for _ in range(nb_vert_splits):
                rect = Rect(x, y, split_width, split_height)
                splits.append(Frame(rect, frame.number, len(splits)))
                x += split_width
            y += split_height
        return splits

    def setup_image(self, im, bg):

        if self._debug:
            self._debug_images = [im]

        bg_luminance = (bg[0] * 299 + bg[1] * 587 + bg[2] * 114) / 1000
        self._bg = bg

        # Contert to grayscale.
        im = im.convert(mode='L')
        if self._debug:
            self._debug_images.append(im)

        # Convert to 2 tones: background, and the rest.
        table = []
        for n in xrange(256):
            if n < bg_luminance - self._luminance_threshold or \
               n > bg_luminance + self._luminance_threshold:
                n = 255
            else:
                n = 0
            table.append(n)
        im = im.point(table)
        if self._debug:
            self._debug_images.append(im)

        self._image_width, self._image_height = im.size
        self._min_frame_width = max(64, self._image_width / 16)
        self._min_frame_height = max(64, self._image_height / 16)
        if _using_fastcore:
            self._image = im.tostring()
        else:
            self._image = im.getdata()

        rect = Rect(0, 0, self._image_width, self._image_height)
        frames = self._find_frames(rect)
        if frames is None:
            self._frames = [Frame(rect, 0, None)]
        else:
            self._frames = [Frame(rect, n, None) for n, rect in enumerate(frames)]
        self._current_frames = (0, 0)

    def setup_view(self, x, y, width, height):
        self._view_x = 0
        self._view_y = 0
        self._view_width = width
        self._view_height = height

        frames = []
        for f in self._frames:
            frames.extend(self._split_frame(f, width, height))
        self._frames = frames

    def _walk_frames_no_split(self, start, step):
        next_frame = last_frame = start
        while True:
            next_frame += step
            if next_frame < 0 or next_frame >= len(self._frames):
                return
            nf = self._frames[next_frame]
            lf = self._frames[last_frame]
            # Avoid spilling unto next frame if it's splitted.
            if nf.split is not None and nf.number != lf.number:
                return
            yield next_frame, nf

    def scroll(self, to_frame=None, backward=False):
        if backward:
            step = -1
        else:
            step = +1

        if to_frame is not None:
            if to_frame >= 0:
                next_frame = to_frame
            else:
                next_frame = len(self._frames) + to_frame
            if next_frame < 0 or next_frame >= len(self._frames):
                log.error('Smart scrolling impossible: bad frame number: %u/%u', to_frame, len(self._frames))
                return None
        else:
            if backward:
                last_visible_frame = min(self._current_frames)
            else:
                last_visible_frame = max(self._current_frames)
            vbox = Rect(self._view_x, self._view_y, self._view_width, self._view_height)
            for n, f in self._walk_frames_no_split(last_visible_frame, step):
                if not self._is_rect_inside(f.rect, vbox):
                    break
                last_visible_frame = n
            next_frame = last_visible_frame + step
            if next_frame < 0 or next_frame >= len(self._frames):
                return None

        first_visible_frame = last_visible_frame = next_frame
        bbox = self._frames[next_frame].rect
        for n, f in self._walk_frames_no_split(first_visible_frame, step):
            new_bbox = self._grow_bbox(bbox, f.rect)
            if new_bbox.w > self._view_width or new_bbox.h > self._view_height:
                break
            last_visible_frame = n
            bbox = new_bbox

        self._current_frames = (first_visible_frame, last_visible_frame)

        self._view_x, self._view_y = bbox.x, bbox.y

        return bbox

