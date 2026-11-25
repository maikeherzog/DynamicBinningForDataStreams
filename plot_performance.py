import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/performance.csv")

# Beschriftung für die x-Achse: "ohne Drift" zuerst, dann die Thresholds aufsteigend
df["label"] = df["threshold"].apply(lambda t: "ohne Drift" if pd.isna(t) else str(t))
order = ["ohne Drift"] + [str(t) for t in sorted(df["threshold"].dropna().unique())]

summary = (df.groupby("label")["runtime_s"]
             .agg(["mean", "std"])
             .reindex(order))

x = np.arange(len(order))
colors = ["#9a9a9a"] + ["#2a6fdb"] * (len(order) - 1)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x, summary["mean"], yerr=summary["std"], width=0.6,
       color=colors, capsize=4, ecolor="#555555")

# einzelne Läufe als Punkte
for i, label in enumerate(order):
    werte = df.loc[df["label"] == label, "runtime_s"]
    jitter = np.random.uniform(-0.15, 0.15, len(werte))
    ax.scatter(x[i] + jitter, werte, s=12, color="#1a1a1a", alpha=0.5, zorder=3)

ax.set_xticks(x, order)
ax.set_xlabel("Threshold")
ax.set_ylabel("Laufzeit (s)")
ax.set_title("Laufzeit je Threshold")
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("results/runtime_per_threshold.png", dpi=150)
plt.show()