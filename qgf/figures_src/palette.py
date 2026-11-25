"""One palette for every figure of the EPJ QT paper (24 Nov 2026, CJ: 'put a bit of coherence in the colors in the graphs').

Anchored on Fig. 1 (encodings_objects.png), whose register colours were already set: the same colour means the same thing
in every figure. Colour-blind check (Machado 2009 protan/deutan simulation): EVENT, INK, NEUTRAL and SECOND stay separated
in luminance (protan relative luminance 0.10 / 0.02 / 0.26 / 0.36).

  EVENT    #c0392b  red        atoms at the physical event: beside a space / line end, course termination, beside the gap,
                               chain end, across an empty line; the uncorrected copies (P1) in the press-state contrast
  INK      #2a2a2a  near-black the bulk: inside a word, rest of the window, figure tesserae, chain interior, whole block
  NEUTRAL  #8c8c8c  grey       the reference class: plain courses, isolated combinations, corrected copies (P2);
                               legend proxies for line/marker style
  LIGHT    #d9d9d9  light grey intervals under the null / independent atoms; isolated nodes in a register
  SECOND   #e69f00  amber      a second event class shown beside EVENT: the side-note added in the corrected state
  SEQ      viridis 0-0.8       one sequential map for an ordered quantity (letter distance), never reaching red or amber

Drives (AFM vs FM-like) are separated by panel, hardware vs emulation by marker vs line style, never by colour.
"""
import numpy as np
import matplotlib

EVENT, INK, NEUTRAL, LIGHT, SECOND = "#c0392b", "#2a2a2a", "#8c8c8c", "#d9d9d9", "#e69f00"
SEQ_CMAP = "viridis"

def seq(n, lo=0.0, hi=0.8):
    """n colours from the shared sequential map (dark = small, light = large)."""
    cm = matplotlib.colormaps[SEQ_CMAP]
    return [matplotlib.colors.to_hex(cm(x)) for x in np.linspace(lo, hi, n)]
