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
    response = session.get(url)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    # Extract all <title> tags
    team_name = [title.text for title in soup.find_all("title")][0]
    words_to_remove = [str(year) + " ", " Statistics | Baseball-Reference.com"]

    for word in words_to_remove:
        team_name = team_name.replace(word, "")

    return team_name

def _get_1b_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[1])
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_central_1b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    first_base_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_1b_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        first_base_fielding_stats = pd.concat([first_base_fielding_stats, temp_df], ignore_index = True)

    first_base_fielding_stats["Position"] = "1B"
    return first_base_fielding_stats

def get_pacific_1b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    first_base_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_1b_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        first_base_fielding_stats = pd.concat([first_base_fielding_stats, temp_df], ignore_index = True)

    first_base_fielding_stats["Position"] = "1B"

    return first_base_fielding_stats

def get_1b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_1b_stats = get_pacific_1b_fielding_stats(year)

    central_1b_stats = get_central_1b_fielding_stats(year)

    fielding_1b_stats = pd.concat([central_1b_stats, pacific_1b_stats], ignore_index = True)

    return fielding_1b_stats

def get_1b_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    first_base_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_1b_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            first_base_fielding_stats = pd.concat([first_base_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    first_base_fielding_stats["Position"] = "1B"

    if (len(first_base_fielding_stats) > 0):
        return first_base_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def _get_2b_hidden_table(html: str) -> pd.DataFrame:
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

def get_central_2b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    second_base_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_2b_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        second_base_fielding_stats = pd.concat([second_base_fielding_stats, temp_df], ignore_index = True)

    second_base_fielding_stats["Position"] = "2B"
    return second_base_fielding_stats

def get_pacific_2b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    second_base_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_2b_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        second_base_fielding_stats = pd.concat([second_base_fielding_stats, temp_df], ignore_index = True)

    second_base_fielding_stats["Position"] = "2B"

    return second_base_fielding_stats

def get_2b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_2b_stats = get_pacific_2b_fielding_stats(year)

    central_2b_stats = get_central_2b_fielding_stats(year)

    fielding_2b_stats = pd.concat([central_2b_stats, pacific_2b_stats], ignore_index = True)

    return fielding_2b_stats

def get_2b_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    second_base_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_2b_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            second_base_fielding_stats = pd.concat([second_base_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    second_base_fielding_stats["Position"] = "2B"
    if (len(second_base_fielding_stats) > 0):
        return second_base_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def _get_3b_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[3]) 
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_central_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    third_base_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_3b_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        third_base_fielding_stats = pd.concat([third_base_fielding_stats, temp_df], ignore_index = True)

    third_base_fielding_stats["Position"] = "3B"
    return third_base_fielding_stats

def get_pacific_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    third_base_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_3b_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        third_base_fielding_stats = pd.concat([third_base_fielding_stats, temp_df], ignore_index = True)

    third_base_fielding_stats["Position"] = "3B"

    return third_base_fielding_stats

def get_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_3b_stats = get_pacific_3b_fielding_stats(year)

    central_3b_stats = get_central_3b_fielding_stats(year)

    third_base_fielding_stats = pd.concat([central_3b_stats, pacific_3b_stats], ignore_index = True)

    return third_base_fielding_stats

def get_3b_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    third_base_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_3b_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            third_base_fielding_stats = pd.concat([third_base_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    third_base_fielding_stats["Position"] = "3B"
    if (len(third_base_fielding_stats) > 0):
        return third_base_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def _get_ss_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[4]) 
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_central_ss_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    shortstop_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_ss_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        shortstop_fielding_stats = pd.concat([shortstop_fielding_stats, temp_df], ignore_index = True)

    shortstop_fielding_stats["Position"] = "SS"
    return shortstop_fielding_stats

def get_pacific_ss_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    shortstop_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_ss_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        shortstop_fielding_stats = pd.concat([shortstop_fielding_stats, temp_df], ignore_index = True)

    shortstop_fielding_stats["Position"] = "SS"

    return shortstop_fielding_stats

def get_ss_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_ss_stats = get_pacific_ss_fielding_stats(year)

    central_ss_stats = get_central_ss_fielding_stats(year)

    shortstop_fielding_stats = pd.concat([central_ss_stats, pacific_ss_stats], ignore_index = True)

    return shortstop_fielding_stats

def get_ss_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    shortstop_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_ss_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            shortstop_fielding_stats = pd.concat([shortstop_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    shortstop_fielding_stats["Position"] = "SS"
    if (len(shortstop_fielding_stats) > 0):
        return shortstop_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def _get_of_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[5]) 
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_central_of_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    outfield_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_of_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        outfield_fielding_stats = pd.concat([outfield_fielding_stats, temp_df], ignore_index = True)

    outfield_fielding_stats["Position"] = "OF"
    return outfield_fielding_stats

def get_pacific_of_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    outfield_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_of_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        outfield_fielding_stats = pd.concat([outfield_fielding_stats, temp_df], ignore_index = True)

    outfield_fielding_stats["Position"] = "OF"

    return outfield_fielding_stats

def get_of_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_of_stats = get_pacific_of_fielding_stats(year)

    central_of_stats = get_central_of_fielding_stats(year)

    outfield_fielding_stats = pd.concat([central_of_stats, pacific_of_stats], ignore_index = True)

    return outfield_fielding_stats

def get_of_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    of_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_of_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            of_fielding_stats = pd.concat([of_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    of_fielding_stats["Position"] = "OF"
    if (len(of_fielding_stats) > 0):
        return of_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def _get_p_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[6]) 
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_central_p_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    pitching_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_p_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        pitching_fielding_stats = pd.concat([pitching_fielding_stats, temp_df], ignore_index = True)

    pitching_fielding_stats["Position"] = "P"
    return pitching_fielding_stats

def get_pacific_p_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    pitching_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_p_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        pitching_fielding_stats = pd.concat([pitching_fielding_stats, temp_df], ignore_index = True)

    pitching_fielding_stats["Position"] = "P"

    return pitching_fielding_stats

def get_p_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_p_stats = get_pacific_p_fielding_stats(year)

    central_p_stats = get_central_p_fielding_stats(year)

    pitching_fielding_stats = pd.concat([central_p_stats, pacific_p_stats], ignore_index = True)

    return pitching_fielding_stats

def get_p_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    pitching_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_p_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            pitching_fielding_stats = pd.concat([pitching_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    pitching_fielding_stats["Position"] = "P"
    if (len(pitching_fielding_stats) > 0):
        return pitching_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def _get_c_hidden_table(html: str) -> pd.DataFrame:
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
        second_table_html = str(tables[7]) 
        df = pd.read_html(StringIO(second_table_html))[0]
        
    return df

def get_central_c_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_central_team_links(year)
    catching_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_c_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        catching_fielding_stats = pd.concat([catching_fielding_stats, temp_df], ignore_index = True)

    catching_fielding_stats["Position"] = "C"
    return catching_fielding_stats

def get_pacific_c_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    team_links = _get_pacific_team_links(year)
    catching_fielding_stats = pd.DataFrame()

    for link in team_links:
        url = link
        response = session.get(url)

        html = response.text

        temp_df = _get_c_hidden_table(html)
        temp_df = temp_df.drop(['Notes'], axis=1)

        temp_df.insert(0, 'Year', year)
        temp_df.insert(2, 'Team', _get_team_names(url, year))

        catching_fielding_stats = pd.concat([catching_fielding_stats, temp_df], ignore_index = True)

    catching_fielding_stats["Position"] = "C"

    return catching_fielding_stats

def get_c_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    pacific_c_stats = get_pacific_c_fielding_stats(year)

    central_c_stats = get_central_c_fielding_stats(year)

    catching_fielding_stats = pd.concat([central_c_stats, pacific_c_stats], ignore_index = True)

    return catching_fielding_stats

def get_c_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    current_season = most_recent_season()
    
    if year is None:
        year = current_season
    if year < 1950:
        raise ValueError(
            "This query currently only returns standings until the 1950 Season. "
            "This was the first season where the Pacific and Central Leagues were created. "
            "Try looking at years from 1950 to present."
        )
    if year > current_season:
        raise ValueError("Invalid input. The season for the year entered must have begun. It cannot be greater than the current year.")

    team_links = _get_central_team_links(year) + _get_pacific_team_links(year)
    catching_fielding_stats = pd.DataFrame()  # Initialize empty DataFrame before the loop

    for url in team_links:
        team_name = _get_team_names(url, year)  # Store team name once per iteration
        if team_name == team:
            response = session.get(url)

            html = response.text

            temp_df = _get_c_hidden_table(html)
            temp_df = temp_df.drop(['Notes'], axis=1)

            temp_df.insert(0, 'Year', year)
            temp_df.insert(2, 'Team', _get_team_names(url, year))

            catching_fielding_stats = pd.concat([catching_fielding_stats, temp_df], ignore_index = True)
            break  # Stop iterating once the team is found

    catching_fielding_stats["Position"] = "C"
    if (len(catching_fielding_stats) > 0):
        return catching_fielding_stats
    else:
        raise ValueError(
            "Invalid input. Team could not be found."
        )

def get_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    print("Warning: Due to website restrictions, please be patient when retrieving stats. Apologies for the inconvenience")
    fielding_stats = pd.DataFrame()

    fielding_stats = pd.concat([fielding_stats, get_1b_fielding_stats(year), get_2b_fielding_stats(year), get_3b_fielding_stats(year), get_ss_fielding_stats(year), get_of_fielding_stats(year), get_p_fielding_stats(year), get_c_fielding_stats(year)], ignore_index = True)

    return fielding_stats

def get_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    print("Warning: Due to website restrictions, please be patient when retrieving stats. Apologies for the inconvenience")
    fielding_stats = pd.DataFrame()

    fielding_stats = pd.concat([fielding_stats, get_1b_fielding_stats_by_team(team, year), get_2b_fielding_stats_by_team(team, year), get_3b_fielding_stats_by_team(team, year), get_ss_fielding_stats_by_team(team, year), get_of_fielding_stats_by_team(team, year), get_p_fielding_stats_by_team(team, year), get_c_fielding_stats_by_team(team, year)], ignore_index = True)

    return fielding_stats

def get_pacific_fielding_stats(year: Optional[int]) -> pd.DataFrame:
    print("Warning: Due to website restrictions, please be patient when retrieving stats. Apologies for the inconvenience")
    fielding_stats = pd.DataFrame()

    fielding_stats = pd.concat([fielding_stats, get_pacific_1b_fielding_stats(year), get_pacific_2b_fielding_stats(year), get_pacific_3b_fielding_stats(year), get_pacific_ss_fielding_stats(year), get_pacific_of_fielding_stats(year), get_pacific_p_fielding_stats(year), get_pacific_c_fielding_stats(year)], ignore_index = True)

    return fielding_stats

def get_central_fielding_stats(year: Optional[int] = None) -> pd.DataFrame:
    print("Warning: Due to website restrictions, please be patient when retrieving stats. Apologies for the inconvenience")
    fielding_stats = pd.DataFrame()

    fielding_stats = pd.concat([fielding_stats, get_central_1b_fielding_stats(year), get_central_2b_fielding_stats(year), get_central_3b_fielding_stats(year), get_central_ss_fielding_stats(year), get_central_of_fielding_stats(year), get_central_p_fielding_stats(year), get_central_c_fielding_stats(year)], ignore_index = True)

    return fielding_stats