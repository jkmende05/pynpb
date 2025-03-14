# Batting Stats

This group of functions gets batting stats.

## Get Pacific League Batting Stats
`get_pacific_batting_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get batting stats for all pacific league players.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.batting_stats import get_pacific_batting_stats

# Get pacific league batting stats for the 1952 season
batting = get_pacific_batting_stats(1952)

```

## Get Central League Batting Stats
`get_central_batting_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get batting stats for all central league players.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.batting_stats import get_central_batting_stats

# Get central league batting stats for the most recent season
batting = get_central_batting_stats()

```

## Get All Batting Stats
`get_batting_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get batting stats for all players

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.batting_stats import get_batting_stats

# Get all batting stats for the 2023 season
batting = get_batting_stats(2023)

```

## Get Batting Stats by Team
`get_batting_stats_for_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get batting stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.batting_stats import get_batting_stats_for_team

# Get 2018 batting stats for the Hanshin Tigers
batting = get_batting_stats_for_team("Hanshin Tigers", 2018)
```