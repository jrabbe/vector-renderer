#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math

from math3d import vector2
from renderer import color4

def apply(buf, width, height, preset=3,
          debug_passthrough=False, debug_horzvert=False, debug_pair=False,
          debug_negpos=False, debug_offset=False):
    """
    DEBUG KNOBS
    ----------------------------------------------------------------------------
    All debug knobs draw FXAA-untouched pixels in FXAA computed luma (monochrome).

    FXAA_DEBUG_PASSTHROUGH - Red for pixels which are filtered by FXAA with a
                                yellow tint on sub-pixel aliasing filtered by FXAA.
    FXAA_DEBUG_HORZVERT    - Blue for horizontal edges, gold for vertical edges.
    FXAA_DEBUG_PAIR        - Blue/green for the 2 pixel pair choice.
    FXAA_DEBUG_NEGPOS      - Red/blue for which side of center of span.
    FXAA_DEBUG_OFFSET      - Red/blue for -/+ x, gold/skyblue for -/+ y.


    COMPILE-IN KNOBS
    ----------------------------------------------------------------------------
    FXAA_PRESET - Choose compile-in knob preset 0-5.
    ----------------------------------------------------------------------------
    FXAA_EDGE_THRESHOLD - The minimum amount of local contrast required
            to apply algorithm.
            1.0/3.0  - too little
            1.0/4.0  - good start
            1.0/8.0  - applies to more edges
            1.0/16.0 - overkill
    ----------------------------------------------------------------------------
    FXAA_EDGE_THRESHOLD_MIN - Trims the algorithm from processing darks.
            Perf optimization.
            1.0/32.0 - visible limit (smaller isn't visible)
            1.0/16.0 - good compromise
            1.0/12.0 - upper limit (seeing artifacts)
    ----------------------------------------------------------------------------
    FXAA_SEARCH_STEPS - Maximum number of search steps for end of span.
    ----------------------------------------------------------------------------
    FXAA_SEARCH_ACCELERATION - How much to accelerate search,
            1 - no acceleration
            2 - skip by 2 pixels
            3 - skip by 3 pixels
            4 - skip by 4 pixels
    ----------------------------------------------------------------------------
    FXAA_SEARCH_THRESHOLD - Controls when to stop searching.
            1.0/4.0 - seems to be the best quality wise
    ----------------------------------------------------------------------------
    FXAA_SUBPIX_FASTER - Turn on lower quality but faster subpix path.
            Not recommended, but used in preset 0.
            False - turn off
            True  - turn on
    ----------------------------------------------------------------------------
    FXAA_SUBPIX - Toggle subpix filtering.
            0 - turn off
            1 - turn on
            2 - turn on full (ignores FXAA_SUBPIX_TRIM and CAP)
    ----------------------------------------------------------------------------
    FXAA_SUBPIX_TRIM - Controls sub-pixel aliasing removal.
            1.0/2.0 - low removal
            1.0/3.0 - medium removal
            1.0/4.0 - default removal
            1.0/8.0 - high removal
            0.0     - complete removal
    ----------------------------------------------------------------------------
    FXAA_SUBPIX_CAP - Insures fine detail is not completely removed.
            This is important for the transition of sub-pixel detail,
            like fences and wires.
            3.0/4.0 - default (medium amount of filtering)
            7.0/8.0 - high amount of filtering
            1.0     - no capping of sub-pixel aliasing removal
    """

    if preset == 0:
        edge_threshold = (1.0/4.0)
        edge_threshold_min = (1.0/12.0)
        search_steps = 2
        search_acceleration = 4
        search_threshold = (1.0/4.0)
        subpix = 1
        subpix_faster = 1
        subpix_trim = (2.0/3.0)
        subpix_cap = (1.0/4.0)
    elif preset == 1:
        edge_threshold = (1.0/8.0)
        edge_threshold_min = (1.0/16.0)
        search_steps = 4
        search_acceleration = 3
        search_threshold = (1.0/4.0)
        subpix = 1
        subpix_faster = 0
        subpix_trim = (3.0/4.0)
        subpix_cap = (1.0/4.0)
    elif preset == 2:
        edge_threshold = (1.0/8.0)
        edge_threshold_min = (1.0/24.0)
        search_steps = 8
        search_acceleration = 2
        search_threshold = (1.0/4.0)
        subpix = 1
        subpix_faster = 0
        subpix_trim = (3.0/4.0)
        subpix_cap = (1.0/4.0)
    elif preset == 3:
        edge_threshold = (1.0/8.0)
        edge_threshold_min = (1.0/24.0)
        search_steps = 16
        search_acceleration = 1
        search_threshold = (1.0/4.0)
        subpix = 1
        subpix_faster = 0
        subpix_trim = (3.0/4.0)
        subpix_cap = (1.0/4.0)
    elif preset == 4:
        edge_threshold = (1.0/8.0)
        edge_threshold_min = (1.0/24.0)
        search_steps = 24
        search_acceleration = 1
        search_threshold = (1.0/4.0)
        subpix = 1
        subpix_faster = 0
        subpix_trim = (3.0/4.0)
        subpix_cap = (1.0/4.0)
    elif preset == 5:
        edge_threshold = (1.0/8.0)
        edge_threshold_min = (1.0/24.0)
        search_steps = 32
        search_acceleration = 1
        search_threshold = (1.0/4.0)
        subpix = 1
        subpix_faster = 0
        subpix_trim = (3.0/4.0)
        subpix_cap = (1.0/4.0)
    elif preset == 6:
        edge_threshold = (1.0/8.0)
        edge_threshold_min = (1.0/24.0)
        search_steps = 16
        search_acceleration = 1
        search_threshold = (1.0/4.0)
        subpix = 0
        subpix_faster = 0
        subpix_trim = (3.0/4.0)
        subpix_cap = (1.0/4.0)
    else:
        raise NotImplementedError('The provided preset "' + preset + '" is not supported, choose a value between 0 and 6')

    fxaa = Fxaa(buf, width, height,
                edge_threshold, edge_threshold_min,
                search_steps, search_acceleration, search_threshold,
                subpix, subpix_faster, subpix_trim, subpix_cap)
    out = [None] * (width * height)

    for y in xrange(height):
        for x in xrange(width):
            i = x + y * width
            out[i] = fxaa.pixel_shader(x, y, debug_passthrough, debug_horzvert, debug_pair, debug_negpos, debug_offset)

    return out

class Fxaa(object):

    def __init__(self, buf, width, height,
                 edge_threshold=(1/8), edge_threshold_min=(1/16),
                 search_steps=1, search_acceleration=1, search_threshold=(1/4),
                 subpix=0, subpix_faster=False, subpix_trim=(1/2), subpix_cap=(3/4)):

        self.buf = buf
        self.width = width
        self.height = height
        # self.rcp_frame = vector2.create(1/width, 1/height)
        self.rcp_frame = vector2.create(1, 1)

        self.edge_threshold_min = edge_threshold_min
        self.edge_threshold = edge_threshold

        self.search_steps = search_steps
        self.search_acceleration = search_acceleration
        self.search_threshold = search_threshold

        self.subpix = subpix
        self.subpix_faster = subpix_faster
        self.subpix_trim = subpix_trim
        self.subprix_trim_scale = (1.0 / (1.0 - subpix_trim))
        self.subpix_cap = subpix_cap

    def pixel_shader(self, x, y, debug_passthrough=False, debug_horzvert=False, debug_pair=False, debug_negpos=False, debug_offset=False):
        debug = debug_passthrough or debug_horzvert or debug_pair or debug_negpos or debug_offset

        rgb_n = self.texture_offset(x, y - 1)
        rgb_w = self.texture_offset(x - 1, y)
        rgb_m = self.texture_offset(x, y)
        rgb_e = self.texture_offset(x + 1, y)
        rgb_s = self.texture_offset(x, y + 1)
        luma_n = self.luma(rgb_n)
        luma_w = self.luma(rgb_w)
        luma_m = self.luma(rgb_m)
        luma_e = self.luma(rgb_e)
        luma_s = self.luma(rgb_s)

        range_min = self.luma_min(luma_n, luma_w, luma_m, luma_e, luma_s)
        range_max = self.luma_max(luma_n, luma_w, luma_m, luma_e, luma_s)
        the_range = range_max - range_min

        if debug:
            luma_o = luma_m / (1.0 + (0.587/0.299))

        if the_range < max(self.edge_threshold_min, range_max * self.edge_threshold):
            if debug:
                return self.to_float_3(luma_o)

            return rgb_m

        if self.subpix > 0:
            if self.subpix_faster:
                rgb_l = (rgb_n + rgb_w + rgb_m + rgb_e + rgb_s).scale(1.0 / 5.0)
            else:
                rgb_l = rgb_n + rgb_w + rgb_m + rgb_e + rgb_s

        if self.subpix != 0:
            luma_l =  (luma_n + luma_w + luma_e + luma_s) * 0.25
            range_l = abs(luma_l - luma_m)

        if self.subpix == 1:
            blend_l = max(0.0, (range_l / the_range) - self.subpix_trim) * self.subprix_trim_scale
            blend_l = min(self.subpix_cap, blend_l)
        elif self.subpix == 2:
            blend_l = range_l / the_range

        if debug_passthrough:
            if self.subpix == 0:
                blend_l = 0.0

            return color4.create(1.0, blend_l/self.subpix_cap, 0.0)

        rgb_nw = self.texture_offset(x - 1, y - 1)
        rgb_ne = self.texture_offset(x + 1, y - 1)
        rgb_sw = self.texture_offset(x - 1, y + 1)
        rgb_se = self.texture_offset(x + 1, y + 1)

        if self.subpix_faster == 0 and self.subpix > 0:
            rgb_l += rgb_nw + rgb_ne + rgb_sw + rgb_se
            rgb_l.scale(1/9)

        luma_nw = self.luma(rgb_nw)
        luma_ne = self.luma(rgb_ne)
        luma_sw = self.luma(rgb_sw)
        luma_se = self.luma(rgb_se)

        edge_vert = abs((0.25 * luma_nw) + (-0.5 * luma_n) + (0.25 * luma_ne)) + abs((0.50 * luma_w) + (-1.0 * luma_m) + (0.50 * luma_e)) + abs((0.25 * luma_sw) + (-0.5 * luma_s) + (0.25 * luma_se))
        edge_horz = abs((0.25 * luma_nw) + (-0.5 * luma_w) + (0.25 * luma_sw)) + abs((0.50 * luma_n) + (-1.0 * luma_m) + (0.50 * luma_s)) + abs((0.25 * luma_ne) + (-0.5 * luma_e) + (0.25 * luma_se))

        horz_span = edge_horz >= edge_vert

        if debug_horzvert:
            if horz_span:
                return color4.create(1.0, 0.75, 0.0)
            else:
                return color4.create(0.0, 0.50, 1.0)

        length_sign = -self.rcp_frame.y if horz_span else -self.rcp_frame.x

        if not horz_span:
            luma_n = luma_w
            luma_s = luma_e

        gradient_n = abs(luma_n - luma_m)
        gradient_s = abs(luma_s - luma_m)
        luma_n = (luma_n + luma_m) * 0.5
        luma_s = (luma_s + luma_m) * 0.5

        pair_n = gradient_n >= gradient_s

        if debug_pair:
            if pair_n:
                return color4.create(0.0, 0.0, 1.0)
            else:
                return color4.create(0.0, 1.0, 0.0)

        if not pair_n:
            luma_n = luma_s
            gradient_n = gradient_s
            length_sign *= -1.0

        pos_n = vector2.create(x + (0.0 if horz_span else length_sign * 0.5),
                               y + (length_sign * 0.5 if horz_span else 0.0))
        gradient_n *= self.search_threshold

        pos_p = pos_n.clone()
        off_np = vector2.create(self.rcp_frame.x, 0.0) if horz_span else vector2.create(0.0, self.rcp_frame.y)

        luma_end_n = luma_n
        luma_end_p = luma_n

        done_n = False
        done_p = False

        if self.search_acceleration == 1:
            pos_n += off_np.scale(-1.0)
            pos_p += off_np.scale(1.0)
        elif self.search_acceleration == 2:
            pos_n += off_np.scale(-1.5)
            pos_p += off_np.scale(1.5)
            off_np = off_np.scale(2.0)
        elif self.search_acceleration == 3:
            pos_n += off_np.scale(-2.0)
            pos_p += off_np.scale(2.0)
            off_np = off_np.scale(3.0)
        elif self.search_acceleration == 4:
            pos_n += off_np.scale(-2.5)
            pos_p += off_np.scale(2.5)
            off_np = off_np.scale(4.0)

        for i in xrange(self.search_steps):
            if not done_n:
                luma_end_n = self.luma(self.texture_offset(pos_n.x, pos_n.y) if self.search_acceleration == 1 else self.texture_grad(pos_n.x, pos_n.y, off_np))

            if not done_p:
                luma_end_p = self.luma(self.texture_offset(pos_p.x, pos_p.y) if self.search_acceleration == 1 else self.texture_grad(pos_p.x, pos_p.y, off_np))

            done_n = done_n or (abs(luma_end_n - luma_n) >= gradient_n)
            done_p = done_p or (abs(luma_end_p - luma_n) >= gradient_n)

            if done_n and done_p:
                break

            if not done_n:
                pos_n -= off_np

            if not done_p:
                pos_p += off_np

        dst_n = x - pos_n.x if horz_span else y - pos_n.y
        dst_p = x - pos_p.x if horz_span else y - pos_p.y
        direction_n = dst_n < dst_p

        if debug_negpos:
            if direction_n:
                return color4.create(1.0, 0.0, 0.0)
            else:
                return color4.create(0.0, 0.0, 1.0)

        luma_end_n = luma_end_n if direction_n else luma_end_p

        if ((luma_m - luma_n) < 0.0) == ((luma_end_n - luma_n) < 0.0):
            length_sign = 0.0

        span_length = dst_p + dst_n
        # if span_length == 0:
        #     print '''
        #     ABOUT TO DIE:
        #     - dst_p = {}
        #     - dst_n = {}
        #     - x = {}
        #     - y = {}
        #     - horz_span = {}
        #     - pos_n = {}
        #     - pos_p = {}
        #     - off_np = {}
        #     - length_sign = {}
        #     '''.format(dst_p, dst_n, x, y, horz_span, pos_n, pos_p, off_np, length_sign)

        dst_n = dst_n if direction_n else dst_p
        # TODO: figure out why span_length can become zero causing DIV0 errors...
        sub_pixel_offset = 0.0 if length_sign == 0 or span_length == 0 else (0.5 + (dst_n * (-1.0 / span_length))) * length_sign

        if debug_offset:
            ox = 0.0 if horz_span else sub_pixel_offset * 2.0
            oy = sub_pixel_offset * 2.0 if horz_span else 0.0
            if ox < 0.0:
                return self.lerp_3(self.to_float_3(luma_o), color4.create(1.0, 0.0, 0.0), -ox)
            if ox > 0.0:
                return self.lerp_3(self.to_float_3(luma_o), color4.create(0.0, 0.0, 1.0), ox)
            if oy < 0.0:
                return self.lerp_3(self.to_float_3(luma_o), color4.create(1.0, 0.6, 0.2), -oy)
            if oy > 0.0:
                return self.lerp_3(self.to_float_3(luma_o), color4.create(0.2, 0.6, 1.0), oy)

        rgb_f = self.texture_offset(x + (0.0 if horz_span else sub_pixel_offset), y + (sub_pixel_offset if horz_span else 0.0))

        if self.subpix == 0:
            return rgb_f
        else:
            return self.lerp_3(rgb_l, rgb_f, blend_l)

    def sel_3(self, f, t, b):
        return f if b else t

    def to_float_3(self, a):
        return color4.create(a, a, a)

    def lerp_3(self, a, b, amount):
        # TODO: figure out how to do proper interpolation of multi-value objects
        return b.scale(1-amount, scale_alpha=True) + a.scale(amount, scale_alpha=True)

    def luma(self, rgb):
        if rgb is None:
            return None

        return rgb.g * (0.587/0.299) + rgb.r

    def texture_grad(self, x, y, grad):
        # TODO: implement gradient calculation of value
        return self.texture_offset(x, y)

    def texture_offset(self, x, y):
        # TODO: get interpolated if x and y are sub-pixel values
        i = int(round(x + y * self.width))

        if i < 0 or i >= len(self.buf):
            return None

        return self.buf[i]

    def luma_min(self, *vals):
        result = None

        for val in vals:
            if val is None:
                continue

            if result is None or val < result:
                result = val;

        return result

    def luma_max(self, *vals):
        result = None

        for val in vals:
            if val is None:
                continue

            if result is None or val > result:
                result = val;

        return result
