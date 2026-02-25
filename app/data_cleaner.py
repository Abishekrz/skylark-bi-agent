import pandas as pd


def extract_and_map(raw_data, column_map):
    try:
        items = raw_data["data"]["boards"][0]["items_page"]["items"]
    except:
        return pd.DataFrame()

    structured = []

    for item in items:
        row = {"name": item["name"]}

        for col in item["column_values"]:
            col_id = col["id"]

            if col_id in column_map:
                mapped_name = column_map[col_id]
                row[mapped_name] = col["text"]

        structured.append(row)

    df = pd.DataFrame(structured)
    return df