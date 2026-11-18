"""Example: load the Talenta sample delay dataset and summarise delays.

Requires Python 3 and pandas.  Run from the package folder:
    python examples/example_usage.py
"""
from pathlib import Path
import pandas as pd

CSV = Path(__file__).resolve().parent.parent / "talenta-gtfs-delay-sample-v1.0.csv"
SLOTS = ["0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-24"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

df = pd.read_csv(CSV)
print(f"{len(df)} rows, {df['delay'].isna().sum()} without delay value")

# Turn the one-hot columns back into readable labels
df["time_slot"] = df[SLOTS].idxmax(axis=1).where(df[SLOTS].sum(axis=1) == 1)
df["weekday"] = df[DAYS].idxmax(axis=1)

valid = df.dropna(subset=["delay"])
print("\nMean and median delay per origin-destination pair:")
print(valid.groupby(["Origin", "Destination"])["delay"].agg(["count", "mean", "median"]).round(2).to_string())

print("\nMedian delay per scheduled time slot:")
print(valid.groupby("time_slot")["delay"].median().reindex(SLOTS).dropna().to_string())
