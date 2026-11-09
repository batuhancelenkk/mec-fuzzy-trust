"""Normalized trust memberships and Mamdani inference for a single engine."""

from math import isfinite


def memberships(score: float, *, include_medium: bool) -> dict[str, float]:
    """Return the membership degrees of a finite score in [0, 1]."""
    if not isfinite(score) or not 0 <= score <= 1:
        raise ValueError("Trust score must be finite and within [0, 1].")

    if not include_medium:
        return {"L": 1 - score, "H": score}

    return {
        "L": max(0.0, 1 - 2 * score),
        "M": 1 - abs(2 * score - 1),
        "H": max(0.0, 2 * score - 1),
    }


def infer(
    left: float,
    right: float,
    rules: dict[tuple[str, str], str],
    *,
    include_medium: bool,
) -> float:
    """Apply min–max inference and a sampled centroid over [0, 1]."""
    left_degrees = memberships(left, include_medium=include_medium)
    right_degrees = memberships(right, include_medium=include_medium)
    activation = dict.fromkeys(("L", "M", "H"), 0.0)

    for (left_label, right_label), output_label in rules.items():
        strength = min(left_degrees[left_label], right_degrees[right_label])
        activation[output_label] = max(activation[output_label], strength)

    weighted_sum = 0.0
    total_weight = 0.0
    for index in range(1001):
        point = index / 1000
        output_degrees = memberships(point, include_medium=True)
        weight = max(
            min(degree, activation[label])
            for label, degree in output_degrees.items()
        )
        weighted_sum += point * weight
        total_weight += weight

    if total_weight == 0:
        raise ValueError("No fuzzy rule activated for the given inputs.")
    return weighted_sum / total_weight
