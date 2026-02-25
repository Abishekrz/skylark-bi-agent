import os
import json
from openai import OpenAI

# Load key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def interpret_and_analyze(question, deals_df, work_orders_df=None):

    if not OPENROUTER_API_KEY:
        return "OPENROUTER_API_KEY not configured."

    # Limit rows to avoid token overflow
    deals_json = deals_df.head(40).to_dict(orient="records")
    work_json = work_orders_df.head(40).to_dict(orient="records") if work_orders_df is not None else []

    prompt = f"""
You are a CFO-level Business Intelligence analyst.

User Question:
{question}

Deals Data:
{json.dumps(deals_json)}

Work Orders Data:
{json.dumps(work_json)}

Instructions:
1. Calculate active pipeline value.
2. Calculate weighted forecast.
3. Calculate closed revenue.
4. Identify strategic risks.
5. Identify data quality issues.
6. Provide concise executive summary.
"""

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert business intelligence analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"DeepSeek Error: {str(e)}"