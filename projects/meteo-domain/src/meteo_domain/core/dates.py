import datetime

import numpy as np


def to_datetime(date: np.datetime64) -> datetime.datetime:
    """
    https://gist.github.com/blaylockbk/1677b446bc741ee2db3e943ab7e4cabd?permalink_comment_id=3775327

    Converts a numpy datetime64 object to a python datetime object
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = (date - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
    return datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
