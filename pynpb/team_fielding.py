import requests
import pandas as  pd
from io import StringIO
import numpy as np

from typing import List, Optional

from bs4 import BeautifulSoup, Comment

from .utils import most_recent_season
from .data_sources.baseball_reference import baseball_reference_session

session = baseball_reference_session()

def _get_link(url: str, year: int) -> str:
    response = session.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')

    table = table[0]

    for row in table.find_all('tr'):
        cols = row.find_all(['th', 'td'])  # Year is in <th>, other data in <td>

        if len(cols) > 1:  # Ensure there is at least one column
            year_text = cols[0].text.strip()  # Extract year from first column
            if year_text.isdigit() and int(year_text) == year:  # Match integer year
                
                # Get the link from the year column (first column)
                year_a_tag = cols[0].find('a')
                if year_a_tag and 'href' in year_a_tag.attrs:
                    return f"https://www.baseball-reference.com{year_a_tag['href']}"

    return None 

def _get_pacific_link(year: int) -> str:
    url = f'https://www.baseball-reference.com/register/league.cgi?code=JPPL&class=Fgn'

    link = _get_link(url, year)

    return link

def _get_central_link(year: int) -> str:
    url = f'https://www.baseball-reference.com/register/league.cgi?code=JPCL&class=Fgn'

    link = _get_link(url, year)

    return link

def _get_third_hidden_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    # Find all tables inside those comments directly
    tables = []

    # Iterate through the comments and extract tables
    for comment in comments:
        comment_soup = BeautifulSoup(comment, "html.parser")
        tables_in_comment = comment_soup.find_all("table")
        if tables_in_comment:
            tables.extend(tables_in_comment)

    if len(tables) >= 2:
        second_table_html = str(tables[2])  # second hidden table
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_pacific_team_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get pacific league team fielding stats
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the pacific league team fielding stats from the year entered.
    """

    if year is None:
        year = most_recent_season()
    if year < 2005:
        raise ValueError(
                "This query currently only returns team fielding stats after the 2005 Season. "
                "Try looking at years from 2005 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )
    
    link = _get_pacific_link(year)
    response = session.get(link)

    html = response.text
    pacific_team_fielding = _get_third_hidden_table(html)

    # Get team stats and apply modifications to make it easier to read
    pacific_team_fielding = pacific_team_fielding.drop(columns=['Aff', 'Attendance'], errors='ignore')
    pacific_team_fielding = pacific_team_fielding.rename(columns={'Tm' : 'Team', 'PO.1' : 'PO', 'Finals' : 'Team'})
    pacific_team_fielding = pacific_team_fielding.iloc[:-1]  # Keeps all rows except the last one

    return pacific_team_fielding

def get_central_team_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get central league team fielding stats
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the central league team fielding stats from the year entered.
    """

    if year is None:
        year = most_recent_season()
    if year < 2005:
        raise ValueError(
                "This query currently only returns team fielding stats after the 2005 Season. "
                "Try looking at years from 2005 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )
    
    link = _get_central_link(year)
    response = session.get(link)

    html = response.text
    central_team_fielding = _get_third_hidden_table(html)

    # Get team stats and apply modifications to make it easier to read
    central_team_fielding = central_team_fielding.drop(columns=['Aff', 'Attendance'], errors='ignore')
    central_team_fielding = central_team_fielding.rename(columns={'Tm' : 'Team', 'Finals' : 'Team', 'PO.1' : 'PO'})
    central_team_fielding = central_team_fielding.iloc[:-1]  # Keeps all rows except the last one

    return central_team_fielding

def get_team_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get team fielding stats
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the team fielding stats from the year entered.
    """

    central_team_fielding = get_central_team_fielding_stats(year)
    pacific_team_fielding = get_pacific_team_fielding_stats(year)

    # Get central and pacific stats, and combine into one dataframe
    team_fielding_stats = pd.concat([central_team_fielding, pacific_team_fielding], ignore_index=True)

    return team_fielding_stats