"""Genera le icone della Livella (PNG, senza dipendenze esterne).

Uso:  python3 tools/make-icons.py livella/icons
"""

import zlib, struct, math, sys

def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)

def smoothstep(e0, e1, x):
    t = clamp((x - e0) / (e1 - e0))
    return t * t * (3 - 2 * t)

def mix(c1, c2, a):
    return tuple(c1[i] * (1 - a) + c2[i] * a for i in range(3))

def write_png(path, size, pixel_fn):
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            r, g, b = pixel_fn(x + 0.5, y + 0.5)
            raw.append(int(clamp(r) * 255 + 0.5))
            raw.append(int(clamp(g) * 255 + 0.5))
            raw.append(int(clamp(b) * 255 + 0.5))
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    open(path, 'wb').write(png)

def make(path, size):
    S = float(size)
    cx = cy = S / 2.0
    aa = S / 512.0 * 1.6          # antialias width in px
    R_outer = 0.335 * S           # outer ring radius
    W_outer = 0.030 * S           # outer ring stroke
    R_target = 0.175 * S          # target ring radius
    W_target = 0.022 * S
    R_bubble = 0.088 * S
    bx, by = cx + 0.045 * S, cy - 0.040 * S   # bubble slightly off-centre

    BG_TOP = (0.078, 0.102, 0.141)
    BG_BOT = (0.024, 0.035, 0.055)
    RING = (0.42, 0.47, 0.55)
    GREEN = (0.18, 0.86, 0.50)
    GREEN_D = (0.08, 0.55, 0.33)

    def px(x, y):
        # background vertical gradient
        col = mix(BG_TOP, BG_BOT, clamp(y / S))
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy)
        # subtle inner glow
        col = mix(col, (0.11, 0.16, 0.22), 0.55 * (1 - smoothstep(0.0, 0.42 * S, d)))
        # crosshair
        cross_len = 0.30 * S
        cw = 0.011 * S
        for (ax, ay) in ((abs(dx), abs(dy)), (abs(dy), abs(dx))):
            a = (1 - smoothstep(cw - aa, cw + aa, ay)) * (1 - smoothstep(cross_len - aa, cross_len + aa, ax))
            col = mix(col, RING, 0.5 * a)
        # outer ring
        a = 1 - smoothstep(W_outer / 2 - aa, W_outer / 2 + aa, abs(d - R_outer))
        col = mix(col, RING, 0.85 * a)
        # target ring
        a = 1 - smoothstep(W_target / 2 - aa, W_target / 2 + aa, abs(d - R_target))
        col = mix(col, GREEN_D, 0.95 * a)
        # bubble glow + body
        db = math.hypot(x - bx, y - by)
        glow = 1 - smoothstep(R_bubble, R_bubble * 2.1, db)
        col = mix(col, GREEN, 0.20 * glow)
        a = 1 - smoothstep(R_bubble - aa, R_bubble + aa, db)
        body = mix(GREEN, (0.62, 0.98, 0.78), clamp(0.55 - (x - bx + y - by) / (2.6 * R_bubble)))
        col = mix(col, body, a)
        return col

    write_png(path, size, px)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'livella/icons'
    for s in (180, 192, 512):
        make(out + '/icon-%d.png' % s, s)
        print('scritta ' + out + '/icon-%d.png' % s)
