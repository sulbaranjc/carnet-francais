"""Render vector illustrations used by the static site.

The PDF and the website share the same ReportLab drawing functions. Rendering
from that source prevents the two versions from drifting apart.
"""

from pathlib import Path
import shutil
import subprocess
import sys

from reportlab.pdfgen import canvas

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_SOURCE = PROJECT_ROOT / "scripts" / "generate_pdf.py"
IMAGES_DIR = PROJECT_ROOT / "assets" / "images"
WORK_DIR = PROJECT_ROOT / ".tmp" / "illustration-render"
SCENE_SIZE = (165, 150)
DPI = 144


def load_drawings():
    """Load drawing helpers without executing the PDF export section."""
    source = PDF_SOURCE.read_text(encoding="utf-8")
    definitions, separator, _ = source.partition("c = canvas.Canvas")
    if not separator:
        raise RuntimeError("PDF drawing source has no canvas entry point.")

    namespace = {"__file__": str(PDF_SOURCE), "__name__": "illustration_source"}
    exec(compile(definitions, str(PDF_SOURCE), "exec"), namespace)
    return namespace


def render_family_scene(name, aunt):
    drawings = load_drawings()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = WORK_DIR / f"{name}.pdf"
    png_prefix = WORK_DIR / name

    document = canvas.Canvas(str(pdf_path), pagesize=SCENE_SIZE)
    drawings["draw_family_scene"](document, 0, 0, aunt=aunt)
    document.save()

    if not shutil.which("pdftoppm"):
        raise RuntimeError("pdftoppm is required to render website illustrations.")

    subprocess.run(
        ["pdftoppm", "-singlefile", "-png", "-r", str(DPI), str(pdf_path), str(png_prefix)],
        check=True,
    )
    shutil.move(str(png_prefix.with_suffix(".png")), IMAGES_DIR / f"{name}.png")


def main():
    render_family_scene("tante", aunt=True)
    render_family_scene("oncle", aunt=False)
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    print("Rendered tante.png and oncle.png.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Illustration rendering failed: {error}", file=sys.stderr)
        raise SystemExit(1)
