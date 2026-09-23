"""SVG to PNG or PDF. Uses whatever the machine has: rsvg-convert, Inkscape, cairosvg, or the
bundled headless-browser renderer in verify/."""
import os, shutil, subprocess

def svg_to_png(svg_path, png_path, scale=2):
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-z", str(scale), "-o", png_path, svg_path], check=True)
        return png_path
    if shutil.which("inkscape"):
        subprocess.run(["inkscape", svg_path, "-o", png_path, "--export-dpi", str(96 * scale)], check=True)
        return png_path
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)
        return png_path
    except ImportError:
        pass
    node = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "verify", "shot.mjs")
    if os.path.exists(node):
        subprocess.run(["node", node, svg_path, png_path, str(scale)], check=True)
        return png_path
    raise RuntimeError("No SVG rasteriser found. Install rsvg-convert, Inkscape or cairosvg, "
                       "or run: node verify/shot.mjs in.svg out.png")
