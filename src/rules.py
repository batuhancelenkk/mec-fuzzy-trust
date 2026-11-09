"""Rule bases transcribed from Table 4 of Ali et al. (2024)."""

# Engine 1 uses DT and RT. Engine 2 uses IT and TT.
PAIR_RULES = {
    ("H", "H"): "H",
    ("H", "L"): "M",
    ("L", "H"): "M",
    ("L", "L"): "L",
}

# Engine 3 uses FO1 and FO2.
FINAL_RULES = {
    ("H", "H"): "H",
    ("H", "M"): "H",
    ("H", "L"): "M",
    ("M", "H"): "H",
    ("M", "M"): "L",
    ("M", "L"): "L",
    ("L", "H"): "M",
    ("L", "M"): "L",
    ("L", "L"): "L",
}
