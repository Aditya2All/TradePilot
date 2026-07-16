import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA).

    Parameters
    ----------
    series : pd.Series
        Price series (usually close prices)
    period : int
        EMA period

    Returns
    -------
    pd.Series
        EMA values
    """
    return series.ewm(span=period, adjust=False).mean()