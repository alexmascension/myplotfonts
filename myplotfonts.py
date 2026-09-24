"""Register TeX Gyre Heros and configure Matplotlib for plotting."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import shutil

import matplotlib as mpl
from matplotlib import font_manager

FONT_BASE_URL = (
    "https://raw.githubusercontent.com/alexmascension/myplotfonts/"
    "main/TeXGyreHeros/"
)
FONT_FILES = {
    "regular": "texgyreheros-regular.otf",
    "bold": "texgyreheros-bold.otf",
    "italic": "texgyreheros-italic.otf",
    "bolditalic": "texgyreheros-bolditalic.otf",
}


def set_plotting_style(cache_dir=None, *, dpi=250):
    """Use TeX Gyre Heros for Matplotlib text and MathText.

    Parameters
    ----------
    cache_dir : str or pathlib.Path, optional
        Font cache directory. Defaults to ``<matplotlib cache>/myplotfonts``.
        Missing fonts are copied from a local checkout if available, otherwise
        downloaded from GitHub. Subsequent calls can run offline.
    dpi : float, default 250
        Figure resolution.

    Returns
    -------
    dict[str, matplotlib.font_manager.FontProperties]
        Font properties for regular, bold, italic and bolditalic text.

    Notes
    -----
    Changes global Matplotlib rcParams. Call after Seaborn/Scanpy style setup.
    MathText configuration applies when ``text.usetex`` is False.
    """
    font_dir = (
        Path(cache_dir).expanduser()
        if cache_dir is not None
        else Path(mpl.get_cachedir()) / "myplotfonts"
    )
    font_dir.mkdir(parents=True, exist_ok=True)
    local_dir = Path(__file__).resolve().parent / "TeXGyreHeros"
    fonts = {}

    for style, filename in FONT_FILES.items():
        font_path = font_dir / filename
        if not font_path.exists():
            # Publish only complete, validated files to the cache.
            temporary_path = None
            try:
                with NamedTemporaryFile(dir=font_dir, suffix=".otf", delete=False) as out:
                    temporary_path = Path(out.name)
                    local_path = local_dir / filename
                    if local_path.is_file():
                        with local_path.open("rb") as source:
                            shutil.copyfileobj(source, out)
                    else:
                        with urlopen(FONT_BASE_URL + filename, timeout=30) as source:
                            shutil.copyfileobj(source, out)
                font_manager.FontProperties(fname=str(temporary_path)).get_name()
                temporary_path.replace(font_path)
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)

        font_manager.fontManager.addfont(str(font_path))
        fonts[style] = font_manager.FontProperties(fname=str(font_path))

    family = fonts["regular"].get_name()
    mpl.rcParams.update({
        "figure.dpi": dpi,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": False,
        "font.family": family,
        "font.sans-serif": [family],
        "font.cursive": [family],
        "mathtext.fontset": "custom",
        "mathtext.rm": family,
        "mathtext.it": f"{family}:italic",
        "mathtext.bf": f"{family}:bold",
        "mathtext.bfit": f"{family}:bold:italic",
        "mathtext.cal": family,
    })
    return fonts
