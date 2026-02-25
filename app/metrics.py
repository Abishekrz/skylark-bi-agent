import pandas as pd


def calculate_pipeline(df):

    df["deal_value"] = pd.to_numeric(df["deal_value"], errors="coerce").fillna(0)
    df["probability"] = pd.to_numeric(df["probability"], errors="coerce").fillna(0)
    df["stage"] = df["stage"].fillna("Unknown")

    # Active pipeline = anything not Won or Lost
    active_df = df[~df["stage"].isin(["Won", "Lost"])]

    total_pipeline = active_df["deal_value"].sum()

    weighted_pipeline = (
        active_df["deal_value"] * (active_df["probability"] / 100)
    ).sum()

    won_revenue = df[df["stage"] == "Won"]["deal_value"].sum()

    return {
        "active_pipeline_value": round(total_pipeline, 2),
        "weighted_pipeline": round(weighted_pipeline, 2),
        "closed_revenue": round(won_revenue, 2)
    }


def sector_breakdown(df):
    df["deal_value"] = pd.to_numeric(df["deal_value"], errors="coerce").fillna(0)
    df["sector"] = df["sector"].fillna("Unknown")

    result = df.groupby("sector")["deal_value"].sum().to_dict()

    return result