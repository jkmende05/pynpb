import requests
import pandas as  pd
from io import StringIO
import numpy as np

from typing import List, Optional

from bs4 import BeautifulSoup, Comment

from .utils import most_recent_season
from .data_sources.baseball_reference import baseball_reference_session

session = baseball_reference_session()

def _get_roster_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[8]) 
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_pacific_player_data(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns player data after the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    roster_data = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_roster_hidden_table(html)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        roster_data = pd.concat([roster_data, temp_df], ignore_index = True)

    return roster_data

def get_central_player_data(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns player data after the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    roster_data = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_roster_hidden_table(html)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        roster_data = pd.concat([roster_data, temp_df], ignore_index = True)

    return roster_data

def get_player_data(year: Optional[int] = None) -> pd.DataFrame:
    pacific_data = get_pacific_player_data(year)

    central_data = get_central_player_data(year)

    player_data = pd.concat([central_data, pacific_data], ignore_index = True)

    return player_data

def get_player_data_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    pacific_data = get_pacific_player_data(year)

    central_data = get_central_player_data(year)

    player_data = pd.concat([central_data, pacific_data], ignore_index = True)

    if len(player_data[player_data['Team'] == team]) > 0:
        player_data = player_data[player_data['Team'] == team].reset_index()
    else:
        team_names = player_data['Team'].unique().tolist()
        raise ValueError(
            "Invalid input. Team could not be found. "
            "Here is a list of valid inputs, which are all the teams that participated in the draft "
            f"in {year}: {team_names}"
        )

    return player_data