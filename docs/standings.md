# Standings

This group of functions gets NPB league standings.

## Get Pacific League Standings
`get_pacific_standings(year: Optional[int] = None) -> pd.DataFrame`

This function will get pacific league standings.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.standings import get_pacific_standings

# Get pacific league stadings for 1967
standings_df = get_pacific_standings(1967)

```

## Get Central League Standings
`get_central_standings(year: Optional[int] = None) -> pd.DataFrame`

This function will get central league standings.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.standings import get_central_standings

# Get central league stadings for 1967
standings_df = get_central_standings(1967)

```

## Get All Standings
`get_all_standings(year: Optional[int] = None) -> List[pd.DataFrame]`

This function will get all standings and store them in a list

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.standings import get_all_standings

# Get all 2024 standings
standings_df = get_all_standings(2024)

```

## Get Combined Standings
`get_combined_standings(year: Optional[int] = None) -> pd.DataFrame`

This function will get the overall league standings.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.standings import get_combined_standings

# Get combined league stadings for 1986
standings_df = get_combined_standings(1986)

```