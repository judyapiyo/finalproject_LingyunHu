# scripts/analysis_matplotlib_beauty.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# 1. Setup: create figures directory
os.makedirs("figures", exist_ok=True)

# 2. Load merged data
df = pd.read_csv("output/merged_data.csv")

# 3. Descriptive statistics & correlation matrix
print("=== Descriptive Statistics ===")
print(df[[
    "Cost of Living Index 2024",
    "MedianHouseholdIncome",
    "Frequent Mental Distress raw value"
]].describe())

print("\n=== Correlation Matrix ===")
print(df[[
    "Cost of Living Index 2024",
    "MedianHouseholdIncome",
    "Frequent Mental Distress raw value"
]].corr())

# 4. Global style settings
plt.style.use("ggplot")
plt.rc("font", family="serif", size=12)
plt.rc("axes", titlesize=16, labelsize=14)
plt.rc("xtick", labelsize=11)
plt.rc("ytick", labelsize=11)

# 5. Plotting function
def plot_beauty(x, y, title, xlabel, ylabel, out_png):
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="#f7f7f7")
    ax.set_facecolor("#fbfbfb")

    # Scatter: red diamonds with black edges
    ax.scatter(x, y,
               marker="D", s=100,
               c="red", edgecolor="black", linewidth=0.8,
               alpha=0.8, zorder=3)

    # Regression line
    coef = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(coef)
    xs = np.linspace(x.min(), x.max(), 200)
    ax.plot(xs, fit_fn(xs),
            color="gold", linewidth=2.5, linestyle="--",
            zorder=2)

    # Fill confidence band (±1.96 * std error)
    y_pred = fit_fn(x)
    resid = y - y_pred
    se = np.std(resid) * np.sqrt(1/len(x) + (x - x.mean())**2/((np.std(x)**2)*len(x)))
    ci = 1.96 * se
    ax.fill_between(x, y_pred - ci, y_pred + ci,
                    color="gold", alpha=0.2, zorder=1)

    # Annotate Pearson r
    r = x.corr(y)
    ax.text(0.05, 0.95,
            f"Pearson $r$ = {r:.2f}",
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor="white", alpha=0.9),
            verticalalignment="top")

    # Highlight top 3 distress points
    top3 = df.nlargest(3, y.name)
    for _, row in top3.iterrows():
        ax.scatter(row[x.name], row[y.name],
                   marker="o", s=150,
                   facecolor="none", edgecolor="darkblue",
                   linewidth=2, zorder=4)
        ax.text(row[x.name], row[y.name] + 0.2,
                row["State"], fontsize=11,
                fontweight="bold", color="darkblue")

    # Axis formatting
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Format large numbers with commas and dollar sign if income
    if "Income" in xlabel:
        ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
    if "Income" in ylabel:
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))

    # Grid: major & minor
    ax.grid(which="major", color="lightgray", linestyle="--", linewidth=0.7, alpha=0.7)
    ax.minorticks_on()
    ax.grid(which="minor", color="lightgray", linestyle=":", linewidth=0.5, alpha=0.5)

    # Remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    fig.savefig(f"figures/{out_png}", dpi=300)
    plt.close(fig)


# 6. Generate and save plots
plot_beauty(
    df["Cost of Living Index 2024"],
    df["Frequent Mental Distress raw value"],
    title="Cost of Living vs. Mental Distress",
    xlabel="Cost of Living Index 2024",
    ylabel="Frequent Mental Distress",
    out_png="cost_vs_distress_beauty.png"
)

plot_beauty(
    df["MedianHouseholdIncome"],
    df["Frequent Mental Distress raw value"],
    title="Income vs. Mental Distress",
    xlabel="Median Household Income",
    ylabel="Frequent Mental Distress",
    out_png="income_vs_distress_beauty.png"
)

plot_beauty(
    df["MedianHouseholdIncome"],
    df["Cost of Living Index 2024"],
    title="Income vs. Cost of Living",
    xlabel="Median Household Income",
    ylabel="Cost of Living Index 2024",
    out_png="income_vs_cost_beauty.png"
)

print("✅ All beautified plots have been saved to the figures/ directory.")
