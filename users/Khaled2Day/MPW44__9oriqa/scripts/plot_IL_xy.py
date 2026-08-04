#!/usr/bin/env python3
"""
Wavelength-sweep plotter, transmission convention (0 dB at top).

Runs in two places without editing:
  * dashboard (Pyodide) -- uses the injected 'test' global, emits base64 PNG
  * command line        -- python plot_il_sweep_dash.py file.xlsx [--linear ...]

Detection is automatic: if 'test' exists in globals, dashboard mode is used.
"""

import io
import base64
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Y-axis convention. Both put 0 dB at the top.
#   False -> Transmission (dB): values negative, axis normal   <- default
#   True  -> Insertion loss (dB): values positive, axis inverted
AS_LOSS = False
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# dashboard plumbing
# ----------------------------------------------------------------------
def emit(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    print("DASH_PLOT_PNG:" + base64.b64encode(buf.getvalue()).decode())
    plt.close(fig)


def pretty(name):
    """'wavelength_nm' -> 'wavelength (nm)'"""
    if "_" in name:
        head, unit = name.rsplit("_", 1)
        return f"{head.replace('_', ' ')} ({unit})"
    return name


def meta_get(meta, *candidates, default=None):
    """Case/space-insensitive metadata lookup, tolerant of key variations."""
    if not meta:
        return default
    norm = {str(k).strip().lower().replace(" ", ""): v for k, v in meta.items()}
    for c in candidates:
        key = c.strip().lower().replace(" ", "")
        if key in norm:
            return norm[key]
        for k, v in norm.items():           # fall back to prefix match
            if k.startswith(key):
                return v
    return default


def clean(values):
    """Replace None with nan so matplotlib gaps the line instead of erroring."""
    return [float("nan") if v is None else float(v) for v in values]


# ----------------------------------------------------------------------
# core plot -- source agnostic
# ----------------------------------------------------------------------
def plot_sweep(sweep, traces, meta=None, xname="wavelength_nm", name="",
               linear=False, xlim=None, annotate=True, as_loss=None):
    """
    sweep  : list of x values
    traces : list of {"name": str, "values": [...]}
    meta   : dict or None
    """
    meta = meta or {}
    as_loss = AS_LOSS if as_loss is None else as_loss

    bits = []
    dev = meta_get(meta, "device_id", "device")
    if dev:
        bits.append(str(dev))
    if name:
        bits.append(str(name))
    src = meta_get(meta, "source_file")
    if src and str(src) != name:
        bits.append(str(src))
    tls = meta_get(meta, "TLSPower (dBm)", "TLSPower")
    if tls is not None:
        bits.append(f"TLS {tls} dBm")
    inst = meta_get(meta, "instrument")
    if inst:
        bits.append(f"instrument: {inst}")
    date = meta_get(meta, "date")
    if date:
        bits.append(str(date))
    title = "  \u00b7  ".join(bits)

    fig, ax = plt.subplots(figsize=(9, 4.6))

    # Work out which sign convention the source data uses, then convert to
    # insertion loss (positive = lossy) as a common internal representation.
    allv = [v for tr in traces for v in clean(tr["values"]) if v == v]
    data_is_loss = (sum(allv) / len(allv)) > 0 if allv else True

    plotted = []
    for tr in traces:
        il = clean(tr["values"])
        if not data_is_loss:
            il = [-v if v == v else v for v in il]

        if linear:
            ys = [10 ** (-v / 10) if v == v else v for v in il]
        elif as_loss:
            ys = il                                    # positive, axis inverted
        else:
            ys = [-v if v == v else v for v in il]     # transmission dB, negative

        ax.plot(sweep, ys, lw=0.9, label=tr.get("name") or "trace")
        plotted.append(ys)

    inverted = (not linear) and as_loss

    if annotate and not linear:
        unit = "dB"
        for ys in plotted:
            finite = [(v, i) for i, v in enumerate(ys) if v == v]
            if not finite:
                continue
            hi_v, hi_i = max(finite)
            lo_v, lo_i = min(finite)
            # on an inverted axis the numerically largest value sits at the bottom
            top = (lo_v, lo_i) if inverted else (hi_v, hi_i)
            bot = (hi_v, hi_i) if inverted else (lo_v, lo_i)
            top_tag = "min IL" if as_loss else "peak"
            bot_tag = "max IL" if as_loss else "min"
            for (val, idx), tag, dy in ((top, top_tag, -30), (bot, bot_tag, 22)):
                ax.annotate(
                    f"{tag} {val:.2f} {unit}\n@ {sweep[idx]:.3f} nm",
                    xy=(sweep[idx], val),
                    xytext=(0, dy),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                    arrowprops=dict(arrowstyle="-", lw=0.6, alpha=0.6),
                )

    ax.set_xlabel(pretty(xname))
    if linear:
        ax.set_ylabel("Transmission (linear)")
    elif as_loss:
        ax.set_ylabel("Insertion loss (dB)")
    else:
        ax.set_ylabel("Transmission (dB)")
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.margins(x=0, y=0.10)
    if xlim:
        ax.set_xlim(*xlim)

    # 0 dB at the top either way: invert the axis for loss, pin the top for dB
    if not linear:
        lo, hi = ax.get_ylim()
        if as_loss:
            ax.set_ylim(bottom=max(lo, hi), top=0)
        else:
            ax.set_ylim(bottom=min(lo, hi), top=0)

    if len(traces) > 1:
        ax.legend(fontsize=9, loc="best")

    fig.tight_layout()
    return fig, ax


def summarise(sweep, traces, meta, name):
    meta = meta or {}
    step = (sweep[-1] - sweep[0]) / (len(sweep) - 1) * 1000 if len(sweep) > 1 else 0
    print(f"Test: {name}")
    print(f"  source     : {meta_get(meta, 'source_file', default='?')}")
    print(f"  date       : {meta_get(meta, 'date', default='?')}")
    print(f"  TLS        : {meta_get(meta, 'TLSPower (dBm)', default='?')} dBm, "
          f"{meta_get(meta, 'TLSOutput', default='?')}, "
          f"{meta_get(meta, 'NumberOfScans', default='?')} scan(s)")
    print(f"  sweep      : {sweep[0]:.3f} - {sweep[-1]:.3f} nm  "
          f"({len(sweep)} pts, {step:.1f} pm step)")
    for tr in traces:
        ys = [v for v in clean(tr["values"]) if v == v]
        if not ys:
            continue
        vmin, vmax = min(ys), max(ys)
        wmin = sweep[clean(tr["values"]).index(vmin)]
        wmax = sweep[clean(tr["values"]).index(vmax)]
        print(f"  {tr.get('name', 'trace'):<12} min {vmin:.3f} dB @ {wmin:.3f} nm   "
              f"max {vmax:.3f} dB @ {wmax:.3f} nm   "
              f"mean {sum(ys)/len(ys):.3f} dB   p-p {vmax - vmin:.3f} dB")


# ----------------------------------------------------------------------
# mode A: dashboard
# ----------------------------------------------------------------------
def run_dashboard(test, linear=False, xlim=None):
    p = test.get("parsed")
    if not p:
        print(f"No parsed data on '{test.get('name', '?')}'.")
        return
    sweep = p["sweep"]["values"]
    xname = p["sweep"].get("name", "wavelength_nm")
    traces = p["traces"]
    meta = test.get("metadata") or {}

    fig, _ = plot_sweep(sweep, traces, meta, xname, test.get("name", ""),
                        linear=linear, xlim=xlim)
    emit(fig)
    summarise(sweep, traces, meta, test.get("name", "?"))


# ----------------------------------------------------------------------
# mode B: command line / xlsx on disk
# ----------------------------------------------------------------------
def run_cli(argv):
    import argparse
    from pathlib import Path
    import pandas as pd

    ap = argparse.ArgumentParser(description="Plot a PAS/OMR wavelength sweep from .xlsx")
    ap.add_argument("xlsx", type=Path)
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--linear", action="store_true")
    ap.add_argument("--as-loss", action="store_true", help="positive IL on an inverted axis")
    ap.add_argument("--xlim", nargs=2, type=float, metavar=("LO", "HI"))
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)

    try:
        md = pd.read_excel(args.xlsx, sheet_name="Metadata")
        meta = dict(zip(md.iloc[:, 0].astype(str), md.iloc[:, 1]))
    except ValueError:
        meta = {}

    sheet = args.sheet
    if sheet is None:
        names = pd.ExcelFile(args.xlsx).sheet_names
        sheet = next((s for s in names if s != "Metadata"), 0)

    df = pd.read_excel(args.xlsx, sheet_name=sheet)
    df = df.dropna(subset=[df.columns[0]]).sort_values(df.columns[0]).reset_index(drop=True)

    sweep = df.iloc[:, 0].tolist()
    xname = str(df.columns[0])
    traces = [{"name": str(c), "values": df[c].tolist()} for c in df.columns[1:]]

    summarise(sweep, traces, meta, args.xlsx.name)
    fig, _ = plot_sweep(sweep, traces, meta, xname, args.xlsx.stem,
                        linear=args.linear, xlim=args.xlim,
                        as_loss=args.as_loss or None)
    if args.out:
        fig.savefig(args.out, dpi=200, bbox_inches="tight")
        print(f"saved -> {args.out}")
    else:
        emit(fig)


# ----------------------------------------------------------------------
if "test" in globals():
    run_dashboard(globals()["test"])          # dashboard mode
elif __name__ == "__main__":
    run_cli(sys.argv[1:])                     # command-line mode