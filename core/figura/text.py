"""Text metrics without a browser.

This is what makes generated figures come out designed rather than approximate: before anything is
drawn, the width of every label is known, so a box can be sized to its content, a font size can be
fitted to a box, and a label can be moved off a collision. Tools that hand layout to an auto-router
cannot do this; tools that draw by hand do it by eye.

Widths are averaged per font class and land within a few percent for Latin text. Where exactness
matters (a tight box, an unusual face), `figura.verify` re-measures in a real browser.
"""
# Average advance width as a fraction of font size, measured across common faces.
RATIO = {"sans": 0.545, "mono": 0.600, "display": 0.500}
# Characters far from the average, as a multiplier on the class ratio.
NARROW = set("iljtIfr.,:;'|!()[]{}- ")
WIDE = set("mwMW@%")

def text_width(t, size, face="sans", tracking=0.0):
    if not t: return 0.0
    r = RATIO.get(face, 0.55)
    w = 0.0
    for ch in t:
        k = 0.62 if ch in NARROW else (1.32 if ch in WIDE else 1.0)
        w += size * r * k
    return w + tracking * max(0, len(t) - 1)

def text_height(size, lines=1, leading=1.35):
    return size * leading * lines if lines > 1 else size * 1.0

def fit_size(t, max_w, start=24, face="sans", minimum=10, tracking=0.0):
    """Largest size <= start whose text fits max_w."""
    s = start
    while s > minimum and text_width(t, s, face, tracking) > max_w:
        s -= 1
    return s

def wrap(t, size, max_w, face="sans", max_lines=None):
    words, lines, cur = t.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and text_width(trial, size, face) > max_w:
            lines.append(cur); cur = w
        else:
            cur = trial
    if cur: lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and text_width(lines[-1] + "...", size, face) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else lines[-1][:-1]
        lines[-1] += "..."
    return lines

def fit_block(t, box_w, box_h, start=24, face="sans", minimum=11, leading=1.35):
    """Largest size at which t wraps inside box_w x box_h. Returns (size, lines)."""
    s = start
    while s >= minimum:
        lines = wrap(t, s, box_w, face)
        if len(lines) * s * leading <= box_h:
            return s, lines
        s -= 1
    return minimum, wrap(t, minimum, box_w, face)
