import requests
from app.config import MONDAY_API_KEY

MONDAY_URL = "https://api.monday.com/v2"

headers = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json"
}


def fetch_board_items(board_id):
    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 500) {{
          items {{
            id
            name
            column_values {{
              id
              text
              value
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        MONDAY_URL,
        json={"query": query},
        headers=headers
    )

    return response.json()