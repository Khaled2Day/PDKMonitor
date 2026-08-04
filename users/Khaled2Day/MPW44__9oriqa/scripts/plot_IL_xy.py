# plot_il_sweep.py — optical wavelength sweep plotter for the web dashboard.
# Paste into the code editor and run. Pyodide-safe: matplotlib + stdlib only.
#
# Default Y axis is transmission dB with 0 dB at the top. Insertion-loss columns
# (positive = lossy) are negated automatically, so either sign convention plots
# the right way up. Change Y_MODE below to switch convention.
#
# This script emits a finished PNG, so its orientation is fixed once drawn --
# nothing downstream re-flips it. The dashboard's separate Spectrum window draws
# its own plot from the parsed numbers and is not affected by this file.
#
# Dashboard globals: test (this file), tests (all files in the folder)

import io
import base64

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------- config ---
Y_MODE     = "transmission"  # "transmission" -> negative dB, 0 at top (default)
                             # "loss"         -> positive dB, axis inverted, 0 at top
                             # "raw"          -> values as supplied, axis untouched
ANNOTATE   = True            # peak / min callouts on the first trace
XLIM       = None            # zoom, e.g. (1540, 1560)
YLIM       = None            # fixed scale, e.g. (-40, 0); None = auto
FIGSIZE    = (9, 4.6)
DEBUG_TINT = False           # True = pink background, to confirm which panel
                             # you are looking at; set back to False afterwards
# -----------------------------------------------------------------------------

NAN = float("nan")


def emit(fig):
    """Hand the figure to the dashboard as a base64 PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    print("DASH_PLOT_PNG:" + base64.b64encode(buf.getvalue()).decode())
    plt.close(fig)


def pretty(name):
    """'Wavelength_nm' -> 'Wavelength (nm)'"""
    if "_" in name:
        head, unit = name.rsplit("_", 1)
        return f"{head.replace('_', ' ')} ({unit})"
    return name


def meta_get(meta, *candidates, default=None):
    """Case/space-insensitive metadata lookup with prefix fallback."""
    if not meta:
        return default
    norm = {str(k).strip().lower().replace(" ", ""): v for k, v in meta.items()}
    for cand in candidates:
        key = cand.strip().lower().replace(" ", "")
        if key in norm:
            return norm[key]
        for k, v in norm.items():
            if k.startswith(key):
                return v
    return default


def to_float(v):
    """None / non-numeric -> nan, so matplotlib gaps the line instead of raising."""
    try:
        return NAN if v is None else float(v)
    except (TypeError, ValueError):
        return NAN


def extremes(xs, ys):
    """Single pass -> ((max_y, max_x), (min_y, min_x)), or None if all nan."""
    hi = lo = None
    for x, y in zip(xs, ys):
        if y != y:
            continue
        if hi is None or y > hi[0]:
            hi = (y, x)
        if lo is None or y < lo[0]:
            lo = (y, x)
    return None if hi is None else (hi, lo)


def read_test(test):
    """-> (sweep, xname, [(name, values)], meta) with x sorted ascending."""
    parsed = test.get("parsed")
    if not parsed or not parsed.get("traces"):
        return None

    sweep = [to_float(v) for v in parsed["sweep"]["values"]]
    xname = parsed["sweep"].get("name") or "Wavelength_nm"
    series = [(tr.get("name") or "trace", [to_float(v) for v in tr["values"]])
              for tr in parsed["traces"]]

    # Drop points with no x, then sort by wavelength so the line never zigzags.
    keep = [i for i, x in enumerate(sweep) if x == x]
    keep.sort(key=lambda i: sweep[i])
    sweep = [sweep[i] for i in keep]
    series = [(n, [vals[i] if i < len(vals) else NAN for i in keep])
              for n, vals in series]

    # Keep only traces holding at least one real point.
    series = [(n, v) for n, v in series if any(y == y for y in v)]
    if not sweep or not series:
        return None

    return sweep, xname, series, (test.get("metadata") or {})


def build_title(name, meta):
    bits = []
    device = meta_get(meta, "device_id", "device")
    if device:
        bits.append(str(device))
    bits.append(str(name))
    tls = meta_get(meta, "TLSPower (dBm)", "TLSPower")
    if tls is not None:
        bits.append(f"TLS {tls} dBm")
    scans = meta_get(meta, "NumberOfScans")
    if scans is not None:
        bits.append(f"{scans} scans")
    date = meta_get(meta, "date")
    if date:
        bits.append(str(date))
    return "  \u00b7  ".join(bits)


def orient(vals, is_loss):
    """Convert source values to whatever Y_MODE asks for."""
    if Y_MODE == "raw":
        return vals
    want_loss = (Y_MODE == "loss")
    if is_loss == want_loss:
        return vals
    return [-y if y == y else y for y in vals]


def plot(test):
    data = read_test(test)
    name = test.get("name", "?")
    if not data:
        print(f"No plottable data on '{name}'.")
        print("Top-level keys:", sorted(test.keys()))
        return

    sweep, xname, series, meta = data

    # Positive mean => the source column is insertion loss.
    finite = [y for _, vals in series for y in vals if y == y]
    is_loss = (sum(finite) / len(finite)) > 0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    if DEBUG_TINT:
        ax.set_facecolor("#ffe9e9")
    drawn = []

    for idx, (tname, vals) in enumerate(series):
        ys = orient(vals, is_loss)
        ax.plot(sweep, ys, lw=0.9, label=tname)
        drawn.append((tname, ys))

        # Callouts on the first trace only, so overlays stay readable.
        if ANNOTATE and idx == 0:
            ends = extremes(sweep, ys)
            if ends:
                inverted = (Y_MODE == "loss")
                top, bottom = (ends[1], ends[0]) if inverted else (ends[0], ends[1])
                for (val, at), tag, dy in ((top, "peak", -30),
                                           (bottom, "min", 22)):
                    ax.annotate(
                        f"{tag} {val:.2f} dB\n@ {at:.3f} nm",
                        xy=(at, val), xytext=(0, dy),
                        textcoords="offset points", ha="center", fontsize=8,
                        arrowprops=dict(arrowstyle="-", lw=0.6, alpha=0.6),
                    )

    ax.set_xlabel(pretty(xname))
    ax.set_ylabel({"transmission": "Transmission (dB)",
                   "loss": "Insertion loss (dB)"}.get(Y_MODE, "Magnitude (dB)"))
    ax.set_title(build_title(name, meta), fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.margins(x=0, y=0.10)
    if XLIM:
        ax.set_xlim(*XLIM)

    # 0 dB at the top for both dB conventions; "raw" is left alone.
    if YLIM:
        ax.set_ylim(*YLIM)
    elif Y_MODE == "transmission":
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom=min(bottom, top), top=0)
    elif Y_MODE == "loss":
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom=max(bottom, top), top=0)      # inverted axis

    if len(drawn) > 1:
        ax.legend(fontsize=9, loc="best")

    fig.tight_layout()
    emit(fig)
    report(name, sweep, drawn, meta, is_loss)


def report(name, sweep, drawn, meta, is_loss):
    step = (sweep[-1] - sweep[0]) / (len(sweep) - 1) * 1000 if len(sweep) > 1 else 0
    print(f"Test: {name}")
    print(f"  source     : {meta_get(meta, 'source_file', default='?')}")
    print(f"  date       : {meta_get(meta, 'date', default='?')}")
    print(f"  TLS        : {meta_get(meta, 'TLSPower (dBm)', default='?')} dBm, "
          f"{meta_get(meta, 'TLSOutput', default='?')}, "
          f"{meta_get(meta, 'NumberOfScans', default='?')} scan(s)")
    print(f"  sweep      : {sweep[0]:.3f} - {sweep[-1]:.3f} nm  "
          f"({len(sweep)} pts, {step:.1f} pm step)")
    print(f"  convention : source was "
          f"{'insertion loss' if is_loss else 'transmission'} "
          f"-> plotted as {Y_MODE}")
    for tname, ys in drawn:
        ends = extremes(sweep, ys)
        if not ends:
            continue
        (hi_v, hi_x), (lo_v, lo_x) = ends
        gaps = sum(1 for y in ys if y != y)
        note = f"   [{gaps} gap(s)]" if gaps else ""
        print(f"  {str(tname):<12} max {hi_v:8.3f} dB @ {hi_x:.3f} nm   "
              f"min {lo_v:8.3f} dB @ {lo_x:.3f} nm   "
              f"p-p {hi_v - lo_v:.3f} dB{note}")


plot(test)