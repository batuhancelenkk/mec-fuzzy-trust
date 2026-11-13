"""Compare trust stability under paired Gaussian input noise."""

import csv
from pathlib import Path
from random import Random
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.baseline.failure_rate import SERVERS
from src.trust import evaluate_trust


SIGMAS = (0.0, 0.02, 0.05, 0.10, 0.15)
TRIALS = 200
SEED = 42
MODELS = {"Dogrusal": False, "Kubik": True}


def scores(profiles, smooth):
    return [evaluate_trust(*profile, smooth=smooth).fo3 for profile in profiles]


def winner(values):
    return max(range(len(values)), key=values.__getitem__)


def run():
    profiles = [server.trust_inputs for server in SERVERS]
    clean = {name: scores(profiles, smooth) for name, smooth in MODELS.items()}
    rng = Random(SEED)
    noise = [
        [[rng.gauss(0, 1) for _ in profile] for profile in profiles]
        for _ in range(TRIALS)
    ]

    for sigma in SIGMAS:
        deviations = {name: [] for name in MODELS}
        switches = dict.fromkeys(MODELS, 0)
        for trial_noise in noise:
            perturbed = [
                [min(1, max(0, value + sigma * z)) for value, z in zip(profile, draws)]
                for profile, draws in zip(profiles, trial_noise)
            ]
            for name, smooth in MODELS.items():
                noisy = clean[name] if sigma == 0 else scores(perturbed, smooth)
                deviations[name].extend(abs(a - b) for a, b in zip(noisy, clean[name]))
                switches[name] += winner(noisy) != winner(clean[name])

        for name in MODELS:
            yield sigma, name, mean(deviations[name]), 100 * switches[name] / TRIALS


def main():
    rows = list(run())
    table = Path("results/tables/noise-robustness.csv")
    figure = Path("results/figures/noise-robustness.png")
    table.parent.mkdir(parents=True, exist_ok=True)
    figure.parent.mkdir(parents=True, exist_ok=True)
    with table.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("sigma", "model", "mean_absolute_fo3_change", "selection_change_pct"))
        for sigma, name, deviation, change in rows:
            writer.writerow((sigma, name, f"{deviation:.6f}", f"{change:.2f}"))

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5), layout="constrained")
    for name, label, style in (("Dogrusal", "Doğrusal", "o-"), ("Kubik", "Kübik", "s--")):
        series = [row for row in rows if row[1] == name]
        for axis, metric in zip(axes, (2, 3)):
            axis.plot(SIGMAS, [row[metric] for row in series], style, label=label)

    for axis, title in zip(axes, ("Ortalama mutlak FO3 sapması", "Sunucu seçimi değişimi (%)")):
        axis.set(xlabel="Gürültü standart sapması (σ)", ylabel=title, ylim=(0, None))
        axis.grid(alpha=0.25)
        axis.legend()
    fig.savefig(figure, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
