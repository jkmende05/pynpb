import requests
import pandas as  pd
from io import StringIO
import numpy as np

from typing import List, Optional

from bs4 import BeautifulSoup
from .utils import most_recent_season

def _get_html(year: int) -> str:
    url = f'https://www.baseball-reference.com/bullpen/{year}_NPB_Active_draft'

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.baseball-reference.com/",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers"
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)

    return response.text

def get_active_draft_results(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1965:
        raise ValueError(
                "This query currently only returns draft results from 2022 and after. "
                "This was the first season where the NPB Active Draft took place"
                "Try looking at years from 2022 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    html = _get_html(year)

    draft_df = pd.read_html(StringIO(html))[0]

    if len(draft_df) == 0:
        # Deal with the case where the season has started or been completed and the amateur draft has not yet taken place
        raise ValueError(
            "No draft results found. Either draft hasn't happened yet or no draft took place this year."
        )

    draft_df = draft_df.drop('Notes', axis=1)

    return draft_df

