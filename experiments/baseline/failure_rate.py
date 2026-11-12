"""Run a synthetic adaptation of the Figure 7(c) failure-rate scenario."""

import random
from statistics import mean
from typing import NamedTuple

from src.trust import evaluate_trust


class Server(NamedTuple):
    trust_inputs: tuple[float, float, float, float]
    normal_failure: float
    unauthorized_failure: float


SERVERS = (
    Server((0.90, 0.85, 0.90, 0.85), 0.05, 0.55),
    Server((0.60, 0.55, 0.55, 0.60), 0.12, 0.75),
    Server((0.25, 0.20, 0.25, 0.20), 0.24, 0.95),
)
REQUESTS = 100
REPETITIONS = 30
SEED = 42


def simulate(unauthorized_count: int, trusted_index: int) -> tuple[float, float]:
    """Return mean failure rates for trust-based and round-robin routing."""
    rng = random.Random(SEED)
    trust_rates = []
    round_robin_rates = []

    for _ in range(REPETITIONS):
        unauthorized_devices = set(rng.sample(range(REQUESTS), unauthorized_count))
        trust_failures = 0
        round_robin_failures = 0

        for device in range(REQUESTS):
            draw = rng.random()
            trust_server = SERVERS[trusted_index]
            round_robin_server = SERVERS[device % len(SERVERS)]
            if device in unauthorized_devices:
                trust_failures += draw < trust_server.unauthorized_failure
                round_robin_failures += draw < round_robin_server.unauthorized_failure
            else:
                trust_failures += draw < trust_server.normal_failure
                round_robin_failures += draw < round_robin_server.normal_failure

        trust_rates.append(trust_failures / REQUESTS)
        round_robin_rates.append(round_robin_failures / REQUESTS)

    return mean(trust_rates), mean(round_robin_rates)


def main() -> None:
    scores = [evaluate_trust(*server.trust_inputs).fo3 for server in SERVERS]
    trusted_index = max(range(len(scores)), key=scores.__getitem__)

    print("# Sentetik görev aktarımı sonuçları")
    print()
    print("Sunucu güven puanları: " + ", ".join(f"{score:.6f}" for score in scores))
    print(f"Güvene göre seçilen sunucu: {trusted_index + 1}")
    print()
    print("| Yetkisiz cihaz | Güvene göre başarısızlık | Sırayla dağıtımda başarısızlık |")
    print("|---:|---:|---:|")
    for count in range(0, REQUESTS + 1, 20):
        trust_rate, round_robin_rate = simulate(count, trusted_index)
        print(f"| {count} | {trust_rate:.2%} | {round_robin_rate:.2%} |")


if __name__ == "__main__":
    main()
