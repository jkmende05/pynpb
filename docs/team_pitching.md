# Team Pitching Stats

This group of functions gets team pitching stats.

## Get Pacific League Team Pitching Stats
`get_pacific_team_pitching_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get team pitching stats for all pacific league teams.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_pitching import get_pacific_team_pitching_stats

# Get pacific league team pitching stats for 1999
pitching_df = get_pacific_team_pitching_stats(1999)

```

## Get Central League Team Pitching Stats
`get_central_team_pitching_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get team pitching stats for all central league teams.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_pitching import get_central_team_pitching_stats

# Get central league team pitching stats for 2005
pitching_df = get_central_team_pitching_stats(2005)

```

## Get All Team Pitching Stats
`get_team_pitching_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all team pitching stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_pitching import get_team_pitching_stats

# Get team pitching stats for the 2023 season
pitching_df = get_team_pitching_stats(2023)

```