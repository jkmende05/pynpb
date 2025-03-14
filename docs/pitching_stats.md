# Pitching Stats

This group of functions gets pitching stats.

## Get Pacific League Pitching Stats
`get_pacific_pitching_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get pitching stats for all pacific league players.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.pitching_stats import get_pacific_pitching_stats

# Get pacific league pitching stats for the 1952 season
pitching = get_pacific_pitching_stats(1952)

```

## Get Central League Pitching Stats
`get_central_pitching_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get pitching stats for all central league players.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.pitching_stats import get_central_pitching_stats

# Get central league pitching stats for the most recent season
pitching = get_central_pitching_stats()

```

## Get All Pitching Stats
`get_pitching_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get pitching stats for all players

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.pitching_stats import get_pitching_stats

# Get pitching stats for the 2023 season
pitching = get_pitching_stats(2023)

```

## Get Pitching Stats by Team
`get_batting_stats_for_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get pitching stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.pitching_stats import get_pitching_stats

# Get 2018 pitching stats for the Hanshin Tigers
pitching = get_pitching_stats("Hanshin Tigers", 2018)
```