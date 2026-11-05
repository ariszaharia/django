from pathlib import Path

from .models import Categorie

_STATIC_DIR = Path(__file__).resolve().parent / "static" / "magazin_app"


def categorii_meniu(request):
    """Categories for the navbar dropdown, available on every page."""
    return {"categorii_meniu": Categorie.objects.all()}


def versiune_static(request):
    """Cache-busting version for our CSS/JS: the newest modification time.

    The dev server sends no cache headers, so browsers keep old stylesheets.
    Appending ?v=<mtime> to the links makes them fetch a file again whenever
    it changes.
    """
    try:
        versiune = max(
            int(f.stat().st_mtime)
            for sub in ("css", "js")
            for f in (_STATIC_DIR / sub).glob("*")
            if f.is_file()
        )
    except ValueError:
        versiune = 0
    return {"static_v": versiune}
