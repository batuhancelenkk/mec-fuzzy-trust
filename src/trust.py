"""Evaluate MEC server trust using the three engines in Table 4."""

import argparse
from typing import NamedTuple

from src.fuzzy import infer, memberships, smooth_memberships
from src.rules import FINAL_RULES, PAIR_RULES


class TrustResult(NamedTuple):
    fo1: float
    fo2: float
    fo3: float


def evaluate_trust(
    dt: float, rt: float, it: float, tt: float, *, smooth: bool = False
) -> TrustResult:
    membership_function = smooth_memberships if smooth else memberships
    fo1 = infer(
        dt, rt, PAIR_RULES, include_medium=False, membership_function=membership_function
    )
    fo2 = infer(
        it, tt, PAIR_RULES, include_medium=False, membership_function=membership_function
    )
    fo3 = infer(
        fo1, fo2, FINAL_RULES, include_medium=True, membership_function=membership_function
    )
    return TrustResult(fo1, fo2, fo3)



def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for score_name in ("dt", "rt", "it", "tt"):
        parser.add_argument(score_name, type=float, help="normalized score in [0, 1]")
    parser.add_argument("--smooth", action="store_true", help="use cubic memberships")
    args = parser.parse_args()

    try:
        result = evaluate_trust(args.dt, args.rt, args.it, args.tt, smooth=args.smooth)
    except ValueError as error:
        parser.error(str(error))

    for label, score in zip(("FO1", "FO2", "FO3"), result):
        print(f"{label} = {score:.6f}")


if __name__ == "__main__":
    main()
