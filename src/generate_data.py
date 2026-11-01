from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "transactions.csv"

RANDOM_SEED = 42
NUMBER_OF_ROWS = 5000


def generate_transactions(
    rows: int = NUMBER_OF_ROWS,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Generate a reproducible synthetic transaction-monitoring dataset."""
    rng = np.random.default_rng(seed)

    customer_ids = [f"CUST{i:05d}" for i in range(1, 801)]

    countries = [
        "India",
        "United States",
        "United Kingdom",
        "Singapore",
        "UAE",
        "Germany",
        "HighRisk-A",
        "HighRisk-B",
    ]

    country_probabilities = [0.42, 0.12, 0.10, 0.08, 0.08, 0.08, 0.06, 0.06]

    channels = ["Web", "Mobile", "Branch", "API"]
    kyc_levels = ["Low", "Medium", "High"]

    start = pd.Timestamp("2026-08-01 00:00:00")
    end = pd.Timestamp("2026-10-31 23:59:59")
    total_seconds = int((end - start).total_seconds())

    timestamps = start + pd.to_timedelta(
        rng.integers(0, total_seconds, size=rows),
        unit="s",
    )

    # Most transactions are modest, with a small long-tail of larger amounts.
    normal_amounts = rng.lognormal(mean=8.0, sigma=0.85, size=rows)
    high_value_mask = rng.random(rows) < 0.04
    normal_amounts[high_value_mask] *= rng.uniform(5, 12, high_value_mask.sum())

    dataframe = pd.DataFrame(
        {
            "transaction_id": [f"TXN{i:07d}" for i in range(1, rows + 1)],
            "customer_id": rng.choice(customer_ids, size=rows),
            "timestamp": timestamps,
            "amount": np.round(normal_amounts, 2),
            "country": rng.choice(
                countries,
                size=rows,
                p=country_probabilities,
            ),
            "channel": rng.choice(
                channels,
                size=rows,
                p=[0.34, 0.45, 0.11, 0.10],
            ),
            "kyc_risk": rng.choice(
                kyc_levels,
                size=rows,
                p=[0.68, 0.24, 0.08],
            ),
            "failed_logins_24h": rng.poisson(lam=0.7, size=rows),
            "chargeback_history": rng.poisson(lam=0.35, size=rows),
            "ip_distance_km": np.round(
                rng.gamma(shape=2.0, scale=260.0, size=rows),
                1,
            ),
            "is_new_payee": rng.choice(
                [0, 1],
                size=rows,
                p=[0.76, 0.24],
            ),
            "velocity_1h": rng.poisson(lam=1.6, size=rows),
            "velocity_24h": rng.poisson(lam=6.0, size=rows),
            "account_age_days": rng.integers(1, 2500, size=rows),
        }
    )

    # Add a small number of deliberately riskier patterns.
    risky_indexes = rng.choice(
        dataframe.index,
        size=max(1, rows // 35),
        replace=False,
    )

    dataframe.loc[risky_indexes, "amount"] *= rng.uniform(
        3.0,
        8.0,
        len(risky_indexes),
    )
    dataframe.loc[risky_indexes, "kyc_risk"] = "High"
    dataframe.loc[risky_indexes, "failed_logins_24h"] += rng.integers(
        3,
        8,
        len(risky_indexes),
    )
    dataframe.loc[risky_indexes, "is_new_payee"] = 1
    dataframe.loc[risky_indexes, "velocity_1h"] += rng.integers(
        4,
        10,
        len(risky_indexes),
    )

    dataframe["amount"] = dataframe["amount"].round(2)
    dataframe = dataframe.sort_values("timestamp").reset_index(drop=True)

    return dataframe


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = generate_transactions()
    dataframe.to_csv(OUTPUT_FILE, index=False)

    print(f"Generated {len(dataframe):,} synthetic transactions.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
