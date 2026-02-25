import pandas as pd
from datetime import datetime
from app.metrics import calculate_pipeline


# ============================================================
# FILTERING FUNCTIONS
# ============================================================

def filter_by_sector(df, sector):
    if sector:
        return df[df["sector"] == sector]
    return df


def filter_by_time(df, time_period):
    if not time_period:
        return df

    df = df.copy()
    df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")

    now = datetime.now()
    current_year = now.year
    current_quarter = (now.month - 1) // 3 + 1

    if time_period == "this_quarter":
        return df[
            (df["close_date"].dt.year == current_year) &
            ((df["close_date"].dt.month - 1) // 3 + 1 == current_quarter)
        ]

    if time_period == "last_quarter":
        last_quarter = current_quarter - 1 if current_quarter > 1 else 4
        year = current_year if current_quarter > 1 else current_year - 1

        return df[
            (df["close_date"].dt.year == year) &
            ((df["close_date"].dt.month - 1) // 3 + 1 == last_quarter)
        ]

    if time_period == "this_year":
        return df[df["close_date"].dt.year == current_year]

    return df
def analyze_execution(deals_df, work_orders_df):

    if deals_df.empty or work_orders_df.empty:
        return "Execution data unavailable."

    closed_deals = deals_df[deals_df["stage"] == "Won"]

    if closed_deals.empty:
        return "No closed deals available for execution analysis."

    matched_projects = work_orders_df[
        work_orders_df["deal_name"].isin(closed_deals["name"])
    ]

    total_projects = len(matched_projects)

    if total_projects == 0:
        return "No matching work orders found for closed deals."

    completed = len(matched_projects[
        matched_projects["project_status"] == "Completed"
    ])

    delayed = len(matched_projects[
        matched_projects["project_status"] == "Delayed"
    ])

    completion_rate = round((completed / total_projects) * 100, 2)

    return f"""
Execution Performance Analysis

• Total Closed Deals: {len(closed_deals)}
• Matching Work Orders: {total_projects}
• Completion Rate: {completion_rate}%
• Delayed Projects: {delayed}

Operational Insight:
• {'Execution efficiency is strong.' if completion_rate > 75 else 'Execution performance requires attention.'}
""".strip()


# ============================================================
# EXECUTIVE SUMMARY ENGINE
# ============================================================

def generate_executive_summary(df, interpretation):

    if df is None or len(df) == 0:
        return (
            "No matching deals found for the requested criteria.\n\n"
            "Consider expanding the time range or reviewing data completeness."
        )

    df = df.copy()

    # -------------------------
    # Safe numeric conversions
    # -------------------------
    df["deal_value"] = pd.to_numeric(df["deal_value"], errors="coerce").fillna(0)

    if "probability" in df.columns:
        df["probability"] = pd.to_numeric(df["probability"], errors="coerce").fillna(0)
    else:
        df["probability"] = 0

    # -------------------------
    # Core metrics
    # -------------------------
    metrics = calculate_pipeline(df)

    total = metrics["active_pipeline_value"]
    weighted = metrics["weighted_pipeline"]
    closed = metrics["closed_revenue"]

    total_deal_value = df["deal_value"].sum()

    # Revenue realization %
    conversion_rate = 0
    if total_deal_value > 0:
        conversion_rate = round((closed / total_deal_value) * 100, 2)

    # Forecast ratio
    forecast_ratio = 0
    if total > 0:
        forecast_ratio = weighted / total

    # Forecast confidence interpretation
    if df["probability"].nunique() <= 1:
        forecast_strength = "limited due to insufficient probability differentiation"
    else:
        forecast_strength = (
            "strong and well-qualified"
            if forecast_ratio > 0.6
            else "moderate"
            if forecast_ratio > 0.3
            else "low-confidence"
        )

    # -------------------------
    # Strategic imbalance detection
    # -------------------------
    imbalance_note = ""

    if closed > total * 3 and total > 0:
        imbalance_note = (
            "Closed revenue significantly exceeds current open pipeline, "
            "suggesting potential near-term pipeline replenishment risk."
        )
    elif total > closed * 3 and closed > 0:
        imbalance_note = (
            "Open pipeline significantly exceeds closed revenue, "
            "indicating strong forward growth potential."
        )

    # -------------------------
    # Strategic signal
    # -------------------------
    if total < closed:
        strategic_signal = (
            "Historical revenue performance is strong relative to current pipeline."
        )
    elif total > closed:
        strategic_signal = (
            "Current pipeline indicates positive forward revenue momentum."
        )
    else:
        strategic_signal = "Pipeline and revenue levels are balanced."

    # -------------------------
    # Data quality checks
    # -------------------------
    missing_sector = df["sector"].isna().sum() if "sector" in df.columns else 0
    total_records = len(df)

    data_quality_note = ""
    if total_records > 0 and missing_sector > 0:
        pct = round((missing_sector / total_records) * 100, 1)
        data_quality_note = (
            f"\n\n⚠ Data Note: {pct}% of deals lack sector classification. "
            "Sector-specific insights may be understated."
        )

    # -------------------------
    # Context header
    # -------------------------
    intent = interpretation.get("intent")
    sector = interpretation.get("sector")
    time_period = interpretation.get("time_period")

    header = "Executive Summary"

    if sector and time_period:
        header = f"Executive Summary – {sector} Sector ({time_period.replace('_', ' ').title()})"
    elif time_period:
        header = f"Executive Summary – {time_period.replace('_', ' ').title()}"
    elif sector:
        header = f"Executive Summary – {sector} Sector"

    # -------------------------
    # Final executive output
    # -------------------------
    summary = f"""
{header}

Pipeline Overview:
• Active Pipeline Value: ₹{total:,.0f}
• Probability-Weighted Forecast: ₹{weighted:,.0f}
• Closed Revenue: ₹{closed:,.0f}

Performance Indicators:
• Forecast confidence appears {forecast_strength}, with {round(forecast_ratio * 100, 2)}% weighted coverage.
• Revenue realization stands at {conversion_rate}% of total deal value.

Strategic Signal:
• {strategic_signal}
"""

    if imbalance_note:
        summary += f"\nRisk Alert:\n• {imbalance_note}\n"

    summary += f"""
Recommendations:
• Accelerate late-stage deal closures to improve forecast reliability.
• Strengthen probability and sector tagging to enhance forecasting accuracy.
{data_quality_note}
"""

    return summary.strip()