from ..geom import Rect
from .. import shapes
from ..text import text_width, fit_size, wrap
from ..style import mix, readable_on

def grid(c, rows, cols, values, area=None, row_label_w=260, cell_render=None, legend_items=None):
    """A comparison or heat grid.

    values[r][c] may be: a string, a bool, a float 0..1 (shaded), or a dict {text, tone}.
    Numbers shade the cell; text is drawn. Anything more than about 8 columns is a table, not a
    figure, and belongs in a document.
    """
    area = area or c.area
    head_h = 52
    cw = (area.w - row_label_w) / len(cols)
    ch = (area.h - head_h) / len(rows)
    for j, col in enumerate(cols):
        x = area.x + row_label_w + j * cw
        c.text(x + cw / 2, area.y + 32, col, size=fit_size(col, cw - 16, 17), weight=600, fill=c.c("ink-2"))
    for i, rlab in enumerate(rows):
        y = area.y + head_h + i * ch
        c.text(area.x, y + ch / 2 + 6, rlab, size=fit_size(rlab, row_label_w - 20, 18), anchor="start")
        c.line((area.x, y), (area.x2, y), c.c("hairline"), 1)
        for j, col in enumerate(cols):
            x = area.x + row_label_w + j * cw
            v = values[i][j]
            cell = Rect(x + 6, y + 6, cw - 12, ch - 12)
            if cell_render: cell_render(c, cell, v); continue
            if isinstance(v, bool):
                c.circle(cell.cx, cell.cy, 9, fill=c.c("good") if v else c.c("hairline"))
            elif isinstance(v, (int, float)):
                shade = mix(c.c("surface"), c.c("accent"), max(0.06, float(v)))
                c.rect(cell, shade, "none", r=6)
                c.text(cell.cx, cell.cy + 6, f"{v:.0%}", size=15,
                       fill=readable_on(shade, c.t, ("ink", "surface")))
            elif isinstance(v, dict):
                shapes.chip(c, cell.cx, cell.cy, v["text"], tone=v.get("tone", "muted"))
            elif v:
                c.text(cell.cx, cell.cy + 6, str(v), size=fit_size(str(v), cell.w - 10, 17), fill=c.c("ink-2"))
    c.line((area.x, area.y2), (area.x2, area.y2), c.c("hairline"), 1)
    if legend_items: shapes.legend(c, area.x, area.y2 + 34, legend_items)
    return area
