import requests
import pandas as  pd
from io import StringIO
import numpy as np

from typing import List, Optional

from bs4 import BeautifulSoup, Comment

from .utils import most_recent_season
from .data_sources.baseball_reference import baseball_reference_session

session = baseball_reference_session()

def _get_stat_links(url: str, year: int) -> List:
    # Return list of team links based on links found in column and row of table
    response = session.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')

    table = table[0]
    # Extract links from the 'team' column where 'year' matches
    team_links = []
    for row in table.find_all('tr'):
        cols = row.find_all(['th', 'td'])  # Year is in <th>, team is in <td>
        if len(cols) > 1:  # Ensure there's at least two columns (year + teams)
            year_text = cols[0].text.strip()  # Extract year from first column
            if year_text.isdigit() and int(year_text) == year:  # Match integer year
                team_col = cols[1]  # The second column contains teams
                for link_tag in team_col.find_all('a'):  # Get all <a> tags inside this column
                    if 'href' in link_tag.attrs:
                        full_link = f"https://www.baseball-reference.com{link_tag['href']}"
                        team_links.append(full_link)
    
    return team_links

def _get_pacific_team_links(year: int) -> List:
    url = f'https://www.baseball-reference.com/register/league.cgi?code=JPPL&class=Fgn'

    team_links = _get_stat_links(url, year)

    return team_links

def _get_central_team_links(year: int) -> List:
    url = f'https://www.baseball-reference.com/register/league.cgi?code=JPCL&class=Fgn'

    team_links = _get_stat_links(url, year)

    return team_links

def _get_team_names(url: str, year: int) -> str:
    # Get team names from the html code
    response = session.get(url)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    # Extract all <title> tags
    team_name = [title.text for title in soup.find_all("title")][0]
    words_to_remove = [str(year) + " ", " Statistics | Baseball-Reference.com"]

    for word in words_to_remove:
        team_name = team_name.replace(word, "")

    return team_name

def get_pacific_pitching_stats(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get pacific league player pitching stats
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the pacific league pitching stats from the year entered.
    """

    if year is None:
        # If year is none, get most recent season
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns pitching stats after the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)

    pitching_stats = pd.DataFrame()
    
    # For each team and link, get data and combine into one dataframe
    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_first_hidden_html_table(html)
        temp_df = temp_df.drop(['Notes', 'Rk'], axis=1)
        temp_df = temp_df.iloc[:-1]
        temp_df['Age'] = temp_df['Age'].astype(int)
        temp_df['Throws'] = temp_df['Name'].apply(lambda x: 'L' if '*' in x else 'S' if '#' in x else 'Unknown' if '?' in x else 'R')
        temp_df['Name'] = temp_df['Name'].str.replace(r'[*?#]', '', regex=True)
        cols = list(temp_df.columns)
        cols.insert(2, cols.pop(cols.index('Throws')))  # Move 'Bats' to index 2 (third position)
        temp_df = temp_df[cols]

        temp_df.insert(0, 'Year', year)
        temp_df.insert(4, 'Team', _get_team_names(url, year))

        pitching_stats = pd.concat([pitching_stats, temp_df], ignore_index = True)

    return pitching_stats

def get_central_pitching_stats(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get central league player pitching stats
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the central league pitching stats from the year entered.
    """

    if year is None:
        # If year is none, get most recent season
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns pitching stats after the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)

    pitching_stats = pd.DataFrame()
    
    # For each team and link, get data and combine into a single dataframe
    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_first_hidden_html_table(html)
        temp_df = temp_df.drop(['Notes', 'Rk'], axis=1)
        temp_df = temp_df.iloc[:-1]
        temp_df['Age'] = temp_df['Age'].astype(int)
        temp_df['Throws'] = temp_df['Name'].apply(lambda x: 'L' if '*' in x else 'S' if '#' in x else 'Unknown' if '?' in x else 'R')
        temp_df['Name'] = temp_df['Name'].str.replace(r'[*?#]', '', regex=True)
        cols = list(temp_df.columns)
        cols.insert(2, cols.pop(cols.index('Throws')))  # Move 'Bats' to index 2 (third position)
        temp_df = temp_df[cols]

        temp_df.insert(0, 'Year', year)
        temp_df.insert(4, 'Team', _get_team_names(url, year))

        pitching_stats = pd.concat([pitching_stats, temp_df], ignore_index = True)

    return pitching_stats

def _get_first_hidden_html_table(html: str) -> pd.DataFrame:
    # Pitching data is the first hidden table in the html code
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find all HTML comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    first_table_html = None
    for comment in comments:
        comment_soup = BeautifulSoup(comment, "html.parser")
        table = comment_soup.find("table")
        if table:
            first_table_html = str(table)
            break

    if first_table_html:
        df = pd.read_html(StringIO(first_table_html))[0]

    return df

def get_pitching_stats(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get player pitching stats
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with pitching stats from the year entered.
    """
    
    central_pitching_stats = get_central_batting_stats(year)

    pacific_pitching_stats = get_pacific_batting_stats(year)

    pitching_stats = pd.concat([central_pitching_stats, pacific_pitching_stats], ignore_index = True)

    return pitching_stats

def get_pitching_stats_for_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    """
    Get pitching stats for a specific team
    
    Parameters
    ----------
    team: str
        A string value representing the team name for which to retrive pitching data.

    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the pitching stats for the team and the year entered.
    """

    # Store `most_recent_season()` in a variable to avoid redundant calls
    current_season = most_recent_season()
    
    if year is None:
        year = current_season

    if year < 1950:
        raise ValueError(
            "This query currently only returns pitching stats after the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    pitching_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)  # Request data only when needed
            html = response.text

            temp_df =  _get_first_hidden_html_table(html)
            temp_df = temp_df.drop(columns=['Notes', 'Rk'], errors='ignore')  # Drop safely

            temp_df = temp_df.iloc[:-1]  # Drop last row
            temp_df['Age'] = temp_df['Age'].astype(int, errors='ignore')  # Convert safely

            # Optimize the 'Bats' column logic
            temp_df['Throws'] = temp_df['Name'].str.extract(r'([*#?])', expand=False).map({'*': 'L', '#': 'S', '?': 'Unknown'}).fillna('R')
            temp_df['Name'] = temp_df['Name'].str.replace(r'[*?#]', '', regex=True)  # Clean names

            # Reorder columns
            cols = list(temp_df.columns)
            cols.insert(2, cols.pop(cols.index('Throws')))  # Move 'Bats' to index 2
            temp_df = temp_df[cols]

            # Add 'Year' and 'Team' columns
            temp_df.insert(0, 'Year', year)
            temp_df.insert(4, 'Team', team_name)

            # Append to final DataFrame
            pitching_stats = pd.concat([pitching_stats, temp_df], ignore_index=True)
            break  # Stop iterating once the team is found

    if (len(pitching_stats) > 0):
        return pitching_stats
    else:
        # If team not found, return value error
        raise ValueError(
            "Invalid input. Team could not be found."
        )