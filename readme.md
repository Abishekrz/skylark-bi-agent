📊 Monday BI Agent

A conversational Business Intelligence API that integrates with monday.com boards to generate executive-ready insights across Deals and Work Orders data.

The system dynamically pulls board data via monday.com GraphQL API, normalizes messy real-world records, and generates structured business summaries including pipeline health, revenue performance, forecast confidence, and operational execution metrics.

🚀 Features

🔌 Live monday.com API integration (read-only)

🧠 Conversational query interpretation

📈 Pipeline & revenue analytics

🏷 Sector-based filtering

📅 Time-based filtering (quarter/year)

⚖ Probability-weighted forecasting

🚨 Strategic risk alerts

📊 Cross-board execution analysis (Deals + Work Orders)

⚠ Data quality transparency

💬 Streamlit conversational UI

🏗 Architecture
Streamlit UI
      ↓
FastAPI Backend (/ask)
      ↓
Query Interpreter
      ↓
Monday.com GraphQL API
      ↓
Data Cleaning & Mapping (Pandas)
      ↓
BI Engine (Metrics + Strategy)
      ↓
Executive Summary Response
🛠 Tech Stack

Backend: FastAPI

Frontend: Streamlit

API Integration: monday.com GraphQL

Data Processing: Pandas

Environment: Python 3.10+

Deployment: Render (or any ASGI-compatible platform)

📁 Project Structure
skylarkdrone/
│
├── app/
│   ├── main.py              # FastAPI app + /ask endpoint
│   ├── config.py            # Environment configuration
│   ├── monday_client.py     # Monday API integration
│   ├── column_mapping.py    # Board column ID mapping
│   ├── data_cleaner.py      # Data extraction & normalization
│   ├── metrics.py           # Pipeline calculations
│   ├── ai_agent.py          # Query interpretation
│   └── bi_engine.py         # Executive summary engine
│
├── streamlit_app.py         # Conversational frontend
├── requirements.txt
└── .env
⚙ Installation
1️⃣ Clone Repository
git clone <repo-url>
cd skylarkdrone
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure Environment Variables

Create a .env file in project root:

MONDAY_API_KEY=your_monday_api_key
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id

Do not use quotes.

▶ Running the Backend
uvicorn app.main:app --reload

Server runs at:

http://127.0.0.1:8000

Test endpoint:

http://127.0.0.1:8000/ask?question=How%20is%20our%20pipeline%20this%20quarter?
▶ Running the Frontend
streamlit run streamlit_app.py
💬 Example Queries

How is our pipeline this quarter?

Show revenue performance this year.

What’s our forecast looking like?

Are we executing closed deals efficiently?

Give me pipeline breakdown by sector.

How is energy sector performing this quarter?

📊 What the BI Engine Computes

Active Pipeline Value

Probability-Weighted Forecast

Closed Revenue

Revenue Realization %

Forecast Confidence

Strategic Imbalance Detection

Risk Alerts

Data Quality Warnings

🔎 Cross-Board Intelligence

The system links:

Deals board (Sales)

Work Orders board (Execution)

It can evaluate:

Closed deal execution performance

Project completion rates

Operational delays

Delivery efficiency

🌍 Deployment
Backend (Render example)

Start command:

uvicorn app.main:app --host 0.0.0.0 --port 10000
Streamlit
streamlit run streamlit_app.py --server.port 10000 --server.address 0.0.0.0

Add environment variables in hosting dashboard.

⚠ Data Handling Notes

All numeric fields are safely coerced.

Dates are normalized.

Missing sector or probability fields are handled gracefully.

The system avoids generating misleading analytics when data is incomplete.

🔮 Future Enhancements

Historical trend comparisons (QoQ)

Visualization dashboard

Advanced NLP intent detection

Forecast variance tracking

Role-based analytics views

Anomaly detection alerts

📌 License

This project is provided for demonstration and educational purposes.