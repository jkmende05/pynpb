# Team Fielding Stats

This group of functions gets team fielding stats.

## Get Pacific League Team Fielding Stats
`get_pacific_team_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get team fielding stats for all pacific league teams.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_fielding import get_pacific_team_fielding_stats

# Get pacific league team fielding stats for 1999
fielding_df = get_pacific_team_fielding_stats(1999)

```

## Get Central League Team Fielding Stats
`get_central_team_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get team fielding stats for all central league teams.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_fielding import get_central_team_fielding_stats

# Get central league team fielding stats for 2005
fielding_df = get_central_team_fielding_stats(2005)

```

## Get All Team Batting Stats
`get_team_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all team fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.team_fielding import get_team_fielding_stats

# Get team fielding stats for the 2023 season
fielding_df = get_team_fielding_stats(2023)

```