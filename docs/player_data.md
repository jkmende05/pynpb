# Player Data

This group of functions gets information about each player, such as birthplace, height, weight and more. 

## Get Pacific League Player Data
`get_pacific_player_data(year: Optional[int] = None) -> pd.DataFrame`

This function will get player data for all pacific league players.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.player_data import get_pacific_player_data

# Get pacific league player data for 2023
player_information = get_pacific_player_data(2023)

```

## Get Central League Player Data
`get_central_player_data(year: Optional[int] = None) -> pd.DataFrame`

This function will get player data for all central league players.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.player_data import get_central_player_data

# Get central league player data for the most recent season
player_information = get_central_player_data()

```

## Get All Player Data
`get_player_data(year: Optional[int] = None) -> pd.DataFrame`

This function will get all player data for the year entered

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.player_data import get_player_data

# Get player data for the 2023 season
player_information = get_player_data(2023)

```

## Get Player Data by Team
`get_player_data_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get player data for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.player_data import get_player_data_by_team

# Get 2024 player data  for the Hanshin Tigers
player_information = get_player_data_by_team("Hanshin Tigers", 2024)
```