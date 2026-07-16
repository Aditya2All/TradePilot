import pandas as pd


def candles_to_dataframe(response: dict) -> pd.DataFrame:
    """
    Convert Upstox historical candle response
    into a pandas DataFrame.
    """

    candles = response["data"]["candles"]

    df = pd.DataFrame(
        candles,
        columns=[
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "open_interest",
        ],
    )

    df["datetime"] = pd.to_datetime(df["datetime"])

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "open_interest",
    ]

    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric
    )

    # Upstox returns newest candle first
    df = df.sort_values("datetime").reset_index(drop=True)

    return df