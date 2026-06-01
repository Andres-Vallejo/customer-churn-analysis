from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_data.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return pd.DataFrame()
    return df[numeric_cols].agg(["count", "sum", "mean", "min", "max"]).T.round(2)


def grouped_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = [c for c in df.columns if c not in numeric_cols]
    if not numeric_cols or not text_cols:
        return pd.DataFrame()
    group_col = text_cols[0]
    return df.groupby(group_col)[numeric_cols].sum(numeric_only=True).reset_index()


def make_chart(grouped: pd.DataFrame) -> None:
    if grouped.empty or grouped.shape[1] < 2:
        return
    x_col = grouped.columns[0]
    y_col = grouped.columns[1]
    ax = grouped.sort_values(y_col, ascending=False).plot(kind="bar", x=x_col, y=y_col, legend=False, figsize=(8, 4))
    ax.set_title(f"{y_col} by {x_col}")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "summary_chart.png", dpi=160)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    summary = numeric_summary(df)
    grouped = grouped_summary(df)
    summary.to_csv(OUTPUT_DIR / "numeric_summary.csv")
    grouped.to_csv(OUTPUT_DIR / "grouped_summary.csv", index=False)
    make_chart(grouped)
    print("Analysis complete. Outputs written to outputs/.")
    print(summary)


if __name__ == "__main__":
    main()
