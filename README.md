# myplotfonts

Set of fonts I usually need for my plots, with a Matplotlib helper for
TeX Gyre Heros (regular, bold, italic and bold italic).

## Installation

```bash
pip install git+https://github.com/alexmascension/myplotfonts.git
```

For a local checkout containing the Python helper:

```bash
pip install -e .
```

## Matplotlib

```python
import matplotlib.pyplot as plt
from myplotfonts import set_plotting_style

fonts = set_plotting_style()

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4])
ax.set_title("TeX Gyre Heros", fontweight="bold")
ax.set_xlabel(r"Time $t$")
ax.set_ylabel(r"$y = t^2$")
ax.text(0.05, 0.9, "Bold italic", transform=ax.transAxes,
        fontproperties=fonts["bolditalic"])
plt.show()
```

`set_plotting_style(cache_dir=None, *, dpi=250)` registers all four font faces
and updates global Matplotlib settings for normal text and MathText. It returns
a dictionary of `FontProperties` keyed by `regular`, `bold`, `italic` and
`bolditalic`. MathText settings apply with `text.usetex=False`; external LaTeX
font configuration is separate. Missing mathematical symbols can use Matplotlib's
fallback fonts.

Fonts are cached under `Path(matplotlib.get_cachedir()) / "myplotfonts"` by
default. A local checkout supplies the fonts directly; otherwise the first call
downloads missing fonts from this repository and requires internet access.
Later calls reuse the cached files, but still register them in the current
Python process. Downloads have a 30-second socket timeout; download and font
validation errors propagate to the caller without caching partial files.

To use a project-specific cache:

```python
from pathlib import Path
fonts = set_plotting_style(cache_dir=Path(".cache") / "fonts", dpi=250)
```

## Seaborn and Scanpy (optional)

Neither library is required. If you use them, configure their style first so
that their settings do not override the font configuration:

```python
import scanpy as sc
import seaborn as sns
from myplotfonts import set_plotting_style

sc.set_figure_params(dpi=250)
sns.set_style("white")
fonts = set_plotting_style()
```

The helper itself sets white figure/axes backgrounds and disables the axes grid;
use Seaborn for its complete `white` theme.
