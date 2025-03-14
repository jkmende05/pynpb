# Team Batting Stats

This group of functions gets team batting stats.

## Get Pacific League Team Batting Stats
`get_pacific_team_batting_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get team batting stats for all pacific league teams.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_batting import get_pacific_team_batting_stats

# Get pacific league team batting stats for 1999
batting_df = get_pacific_team_batting_stats(1999)

```

## Get Central League Team Batting Stats
`get_central_team_batting_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get team batting stats for all central league teams.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_batting import get_central_team_batting_stats

# Get central league team batting stats for 2005
batting_df = get_central_team_batting_stats(2005)

```

## Get All Team Batting Stats
`get_team_batting_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all team batting stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_batting import get_team_batting_stats

# Get team batting stats for the 2023 season
batting_df = get_team_batting_stats(2023)

```