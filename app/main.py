from fastapi import FastAPI
from app.monday_client import fetch_board_items
from app.data_cleaner import extract_and_map
from app.config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID
from app.metrics import calculate_pipeline, sector_breakdown # type: ignore
from app.column_mapping import DEALS_COLUMN_MAP,WORK_ORDERS_COLUMN_MAP
from app.data_cleaner import extract_and_map
from app.ai_agent import interpret_and_analyze
from app.bi_engine import (
    filter_by_sector,
    filter_by_time,
    generate_executive_summary,
    analyze_execution
)
from fastapi import FastAPI
from app.monday_client import fetch_board_items
from app.data_cleaner import extract_and_map
from app.column_mapping import DEALS_COLUMN_MAP, WORK_ORDERS_COLUMN_MAP
from app.config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID
from app.ai_agent import interpret_and_analyze
app = FastAPI()


@app.get("/ask")
def ask(question: str):

    try:
        # -------------------------------------------------
        # 1️⃣ Fetch Data from Monday (Live, Read-Only)
        # -------------------------------------------------
        raw_deals = fetch_board_items(DEALS_BOARD_ID)
        raw_work_orders = fetch_board_items(WORK_ORDERS_BOARD_ID)

        deals_df = extract_and_map(raw_deals, DEALS_COLUMN_MAP)
        work_orders_df = extract_and_map(raw_work_orders, WORK_ORDERS_COLUMN_MAP)

        if deals_df.empty:
            return {
                "error": "No deal data available from Monday board."
            }

        # -------------------------------------------------
        # 2️⃣ Limit Rows (Prevent Token Overflow)
        # -------------------------------------------------
        deals_df_limited = deals_df.head(200)
        work_orders_df_limited = work_orders_df.head(200)

        # -------------------------------------------------
        # 3️⃣ Send to Open-Source AI Agent
        # -------------------------------------------------
        ai_summary = interpret_and_analyze(
            question,
            deals_df_limited,
            work_orders_df_limited
        )

        # -------------------------------------------------
        # 4️⃣ Return Response
        # -------------------------------------------------
        return {
            "question": question,
            "executive_summary": ai_summary
        }

    except Exception as e:
        return {
            "error": "An unexpected error occurred while processing the request.",
            "details": str(e)
        }


@app.get("/")
def home():
    return {"message": "Monday BI Agent Running"}


@app.get("/debug-deals")
def debug_deals():
    raw = fetch_board_items(DEALS_BOARD_ID)
    return raw


@app.get("/debug-work-orders")
def debug_work_orders():
    raw = fetch_board_items(WORK_ORDERS_BOARD_ID)
    return raw

@app.get("/fetch-cleaned-deals")
def fetch_cleaned_deals():
    raw = fetch_board_items(DEALS_BOARD_ID)
    df = extract_and_map(raw, DEALS_COLUMN_MAP)
    return df.to_dict(orient="records")

@app.get("/inspect-deal-columns")
def inspect_deal_columns():
    raw = fetch_board_items(DEALS_BOARD_ID)
    items = raw["data"]["boards"][0]["items_page"]["items"]

    first_item = items[0]

    return first_item["column_values"]

@app.get("/pipeline-summary")
def pipeline_summary():

    raw = fetch_board_items(DEALS_BOARD_ID)
    df = extract_and_map(raw, DEALS_COLUMN_MAP)

    metrics = calculate_pipeline(df)

    missing_probability = df["probability"].isna().sum()
    missing_sector = df["sector"].isna().sum()
    missing_close = df["close_date"].isna().sum()

    return {
        "metrics": metrics,
        "data_quality": {
            "missing_probability": int(missing_probability),
            "missing_sector": int(missing_sector),
            "missing_close_date": int(missing_close)
        }
    }

@app.get("/debug-mapped-deals")
def debug_mapped_deals():
    raw = fetch_board_items(DEALS_BOARD_ID)
    df = extract_and_map(raw, DEALS_COLUMN_MAP)
    return {
        "columns": list(df.columns),
        "sample_rows": df.head(5).to_dict(orient="records")
    }

app = FastAPI()