#   Copyright (c) 2009-2010, Konstantin Yegupov
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without modification,
#   are permitted provided that the following conditions are met:
#
#       * Redistributions of source code must retain the above copyright notice,
#         this list of conditions and the following disclaimer.
#
#       * Redistributions in binary form must reproduce the above copyright notice,
#         this list of conditions and the following disclaimer in the documentation
#         and/or other materials provided with the distribution.
#
#       * The name of the author may not be used to endorse or promote products
#         derived from this software without specific prior written permission. 
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#   ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import glob, os, copy

import Image, ImageDraw

from pprint import pprint

try:
    import psyco
    psyco.full()
except ImportError:
    pass

from ConfigParser import RawConfigParser

from comic_book import ComicBook


leng_threshold = 20


def rect_intersect(r1, r2):
    x0 = max(r1[0],r2[0])
    y0 = max(r1[1],r2[1])
    x1 = min(r1[2],r2[2])
    y1 = min(r1[3],r2[3])
    if x1<x0 or y1<y0:
        return None
    return (x0,y0,x1,y1)

def rect_merge(r1, r2):
    return (min(r1[0],r2[0]),min(r1[1],r2[1]),max(r1[2],r2[2]),max(r1[3],r2[3]))

    
def rect_area(r):
    if r==None:
        return 0
    else:
        return (r[2]-r[0])*(r[3]-r[1])

class MyConfigParser(RawConfigParser):
    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for key in sorted(self._defaults.keys()):
                value = self._defaults[key]
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in sorted(self._sections):
            fp.write("[%s]\n" % section)
            for key in sorted(self._sections[section].keys()):
                if key != "__name__":
                    value = self._sections[section][key]
                    fp.write("%s = %s\n" %
                             (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
       

class Blob:
    def __init__(self):
        self.segs = {}

    def does_touch(self, y, xx):
        if not self.segs.has_key(y-1):
            return False
        for myx0, myx1 in self.segs[y-1]:
            if not (myx1<xx[0] or myx0>xx[1]):
                return True
        return False

    def add(self, y, xx):
        # todo: remove dupes
        try:
            self.segs[y].append(xx)
        except KeyError:
            self.segs[y] = [xx]

    def merge(self, blob2):
        for y, pairs in blob2.segs.iteritems():
            for xx in pairs:
                self.add(y, xx)

    def get_rect(self):
        y0, y1 = 1000000, 0
        x0, x1 = 1000000, 0
        for y, pairs in self.segs.iteritems():
            for xx in pairs:
                if y0>y:
                    y0 = y
                if y1<y:
                    y1 = y
                if x0>xx[0]:
                    x0 = xx[0]
                if x1<xx[1]:
                    x1 = xx[1]
        return (x0,y0,x1,y1)

class CommonSegmentor:

    @classmethod
    def get_border_color(cls, im, s, line):
        # autodetect border color
        xz = im.size[0]-1
        yz = (im.size[1]-1)*line
        histo = {}
        for y in xrange(0, im.size[1]):
            histo.setdefault(s[y*line], 0)
            histo[s[y*line]] += 1
            histo.setdefault(s[y*line+xz], 0)
            histo[s[y*line+xz]] += 1
        for x in xrange(0, im.size[0]):
            histo.setdefault(s[x], 0)
            histo[s[x]] += 1
            histo.setdefault(s[yz+x], 0)
            histo[s[yz+x]] += 1
        pairs = histo.items()
        pairs.sort(key = lambda x: x[1], reverse=True)
        return ord(pairs[0][0])
    
    @classmethod
    def extract_borders(cls, im, border_color=0, tolerance=30, **kwargs):
        s = im.convert("L").tostring()
        line = im.size[0]
       
        if border_color==None:
            border_color = cls.get_border_color(im, s, line)
       
        xrng = range(0, im.size[0])
        blobs = {}
        next_bid = 0
        # First pass - make borderblobs
        for y in xrange(0, im.size[1]):
            sequences = []
            in_border = True
            x0 = 0
            for x in xrng:
                if abs(ord(s[y*line+x])-border_color)<tolerance:
                    if not in_border:
                        x0 = x
                        in_border = True
                elif in_border:
                    sequences.append((x0,x-1))
                    in_border = False
            if in_border:
                sequences.append((x0,im.size[0]-1))
            untouched = set(blobs.keys())
            for seq in sequences:
                touchers = []
                for bid, blob in blobs.iteritems():
                    if blob.does_touch(y, seq):
                        touchers.append(bid)
                        try:
                            untouched.remove(bid)
                        except KeyError:
                            pass
                if len(touchers)==0:
                    newblob = Blob()
                    newblob.add(y, seq)
                    blobs[next_bid] = newblob
                    next_bid += 1
                else:
                    blobs[touchers[0]].add(y, seq)
                    for bid in touchers[1:]:
                        blobs[touchers[0]].merge(blobs[bid])
                        del blobs[bid]
            for bid in untouched:
                del blobs[bid]
        res = []
        bloblist = list(blobs.values())
        
    #    return bloblist
        megablob = bloblist[0]
        for blob in bloblist[1:]:
            megablob.merge(blob)
        return megablob
            
    @classmethod
    def extract_blobs(cls, im, megablob):
        bordsegs = megablob.segs
        # Second pass - extract panel blobs
        blobs = {}
        recent_blobs = set()
        next_bid = 0
        for y in xrange(0, im.size[1]):
            if bordsegs.has_key(y):
                # Calculating border's complement
                segs = bordsegs[y]
                segs.sort(key=lambda x:x[0])
                sequences = []
                lastend = -1
                for seg in segs:
                    if lastend+1<seg[0]:
                        sequences.append((lastend+1, seg[0]-1))
                    lastend = seg[1]
                if lastend<im.size[0]-1:
                    sequences.append((lastend+1, im.size[0]-1))
            else:
                sequences = [(0, im.size[0]-1)]
            new_recent_blobs = set()
            for seq in sequences:
                touchers = []
                for bid in recent_blobs:
                    try:
                        if blobs[bid].does_touch(y, seq):
                            touchers.append(bid)
                    except KeyError:
                        pass
                if len(touchers)==0:
                    newblob = Blob()
                    newblob.add(y, seq)
                    blobs[next_bid] = newblob
                    new_recent_blobs.add(next_bid)
                    next_bid += 1
                else:
                    blobs[touchers[0]].add(y, seq)
                    for bid in touchers[1:]:
                        blobs[touchers[0]].merge(blobs[bid])
                        del blobs[bid]
                        recent_blobs.remove(bid)
                    new_recent_blobs.add(touchers[0])
            recent_blobs = new_recent_blobs
            
        return list(blobs.values())
    
    @classmethod
    def blobs2panels(cls, blobs, min_frame_size=200, auto_edge_snap_limit=20, **kwargs):
    
        rects = []
        
        for blob in blobs: 
            rect = blob.get_rect()
            rects.append(rect)
        rects = cls.remove_overlaps(rects)

        res = []
        for rect in rects:
            if rect[2]-rect[0]<min_frame_size or rect[3]-rect[1]<min_frame_size:
                continue
            res.append(rect)
        
        auto_edge_snap(res, (0,2), auto_edge_snap_limit)
        auto_edge_snap(res, (1,3), auto_edge_snap_limit)
        return res
        
    @classmethod
    def remove_overlaps(cls, rects):
        has_been_merges = True
        while has_been_merges:
            has_been_merges = False
            res = []
            # Remove overlapping
            # Straightforward algo. Can be optimized, I suppose
            unprocessed = set(rects)
            for r1 in rects:
                if r1 not in unprocessed:
                    continue
                overlaps = set()
                overlaps.add(r1)
                overlaps_found = True
                while overlaps_found:
                    overlaps_found = False
                    for r2 in unprocessed:
                        if r2 in overlaps:
                            continue
                        isect = rect_intersect(r1, r2)
                        isect_area = rect_area(isect)
                        if isect_area>0.6*rect_area(r1) or isect_area>0.6*rect_area(r2):
                            overlaps_found = True
                            has_been_merges = True
                            overlaps.add(r2)
                            r1 = rect_merge(r1,r2)
                res.append(r1)
                unprocessed -= overlaps
            rects = res
        return res
    
    @classmethod
    def extract_panels(cls, im, **opts):
        borderblob = cls.extract_borders(im, **opts)
        blobs = cls.extract_blobs(im, borderblob)
        panels = cls.blobs2panels(blobs, **opts)
        return panels

class QCSegmentor:

    @classmethod
    def extract_panels(cls, im, border_color=None, tolerance=4, **kwargs):
        s = im.convert("L").tostring()
        line = im.size[0]
       
        if border_color==None:
            border_color = 0
       
        xrng = range(0, im.size[0])
        
        blacklines = []
        lastblack = -10
        # First pass - black lines
        for y in xrange(0, im.size[1]):
            sequences = []
            in_border = True
            x0 = 0
            for x in xrng:
                if abs(ord(s[y*line+x])-border_color)<tolerance:
                    if not in_border:
                        x0 = x
                        in_border = True
                elif in_border:
                    sequences.append((x0,x-1))
                    in_border = False
            if in_border:
                sequences.append((x0,im.size[0]-1))
            seqlen = sum(x[1]-x[0] for x in sequences)
            if seqlen>0.5*im.size[0]:
                if lastblack == y-1:
                    blacklines[-1][1] += 1
                else:
                    blacklines.append([y, 1])
                lastblack = y
        
        
        rects = []
        y0 = 0
        
        bigblacks = [bl[0]+bl[1]/2 for bl in blacklines if bl[1]>10]
        
        if im.size[1]-51>bigblacks[-1]:
            bigblacks.append(im.size[1]-1)
        else:
            bigblacks[-1] = im.size[1]-1
        for y1 in bigblacks:
            if y1-y0>50:
                rects.append([0,y0,im.size[0]-1,y1])
                y0 = y1
        return rects
            

    
def preview_blobs(im, rects, prevname):
    im_res = im.convert("L").point(lambda x: x//32, "P")
    canv = ImageDraw.Draw(im_res)

    palette = [0]*768;
    for i in xrange(8):
        palette[3*i] = i*36
        palette[3*i+1] = i*36
        palette[3*i+2] = i*36
    palette[24] = 255
    im_res.putpalette(palette)

    for b in rects:
        for y in b.segs:
            for xx in b.segs[y]:
                canv.line(((xx[0],y),(xx[1],y)), fill=8)
    im_res.save(prevname)

def preview_panels(im, rects, prevname):
    im_res = im.convert("L").point(lambda x: x//32, "P")
    canv = ImageDraw.Draw(im_res)

    palette = [0]*768;
    for i in xrange(8):
        palette[3*i] = i*36
        palette[3*i+1] = i*36
        palette[3*i+2] = i*36
    palette[24] = 255
    im_res.putpalette(palette)

    for r in rects:
        canv.rectangle((r[0],r[1],r[2],r[3]), outline=8)
    im_res.save(prevname)

def preview_blobs_and_panels(im, blobs, rects, prevname):
    im_res = im.convert("L").point(lambda x: x//32, "P")
    canv = ImageDraw.Draw(im_res)

    palette = [0]*768;
    for i in xrange(8):
        palette[3*i] = i*36
        palette[3*i+1] = i*36
        palette[3*i+2] = i*36
    palette[24] = 255
    palette[28] = 255
    im_res.putpalette(palette)

    for b in blobs:
        for y in b.segs:
            for xx in b.segs[y]:
                canv.line(((xx[0],y),(xx[1],y)), fill=9)
    for r in rects:
        canv.rectangle((r[0],r[1],r[2],r[3]), outline=8)
    im_res.save(prevname)


def auto_edge_snap(rects, indices, snap=10):
    if len(rects)==0:
        return
    lines = set()
    for r in rects:
        for i in indices:
            lines.add(r[i])
    ls = list(lines)
    ls.sort()
    pl = ls[0]
    snapg = [pl]
    snapmap = {}
    for l in ls[1:]+[1000000]:
        if l-pl<snap:
            snapg.append(l)
        else:
            if len(snapg)>1 and snapg[-1]-snapg[0]<snap*2:
                avg = sum(snapg)/len(snapg)
                for l2 in snapg:
                    snapmap[l2] = avg
            snapg = [l]
        pl = l
    for j,r in enumerate(rects):
        r2 = list(r)
        for i in indices:
            if r2[i] in snapmap:
                r2[i] = snapmap[r2[i]]
        rects[j] = tuple(r2)

def panel_sorter(other, this):
    quadrants = {(-1,-1):-2, (-1,0):-2, (-1,1):-1,
                 (0,-1) :-2, (0,0) : 0, (0,1) : 2,
                 (1,-1) : 1, (1,0) : 2, (1,1) : 2,
                 }
    
    x_quad_range = [0,0] 
    if other[0]<this[0]: x_quad_range[0] = -1
    if other[2]<=this[0]: x_quad_range[1] = -1
    if other[2]>this[2]: x_quad_range[1] = 1
    if other[0]>=this[2]: x_quad_range[0] = 1
    y_quad_range = [0,0] 
    if other[1]<this[1]: y_quad_range[0] = -1
    if other[3]<=this[1]: y_quad_range[1] = -1
    if other[3]>this[3]: y_quad_range[1] = 1
    if other[1]>=this[3]: y_quad_range[0] = 1
    rel = 0
    for xq in range(x_quad_range[0], x_quad_range[1]+1):
        for yq in range(y_quad_range[0], y_quad_range[1]+1):
            rel += quadrants[(yq,xq)]
    return rel
    

def segmentate(opts, comix, page=None, prev_path=None):
    try:
        os.makedirs(os.path.join(prev_path, "seg_preview"))
    except Exception:
        pass
    if page!=None:
        pages = [page]
    else:
        pages = range(len(comix))
    res = []
    segmentor = opts.get("segmentor_class", CommonSegmentor)
    for i in pages: 
        fn = comix.get_filename(i)
        im = Image.open(comix.get_file(i))
        panels = segmentor.extract_panels(im, **opts)
#        panels.sort(key=lambda rect: (rect[1],rect[0]))
        panels.sort(cmp = panel_sorter)
        res.append(panels)
        if prev_path!=None:
            preview_panels(im, panels, os.path.join(prev_path, "seg_preview")+os.sep+fn.replace(".jpg",".png"))
    return res

seg_algos = CommonSegmentor, QCSegmentor


if __name__=="__main__":
    
    try:
        import debug_scripts
    except ImportError:
        debug_scripts = False
    if debug_scripts:
        debug_scripts.go()
