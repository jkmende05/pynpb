# Fielding Stats

This group of functions gets fielding stats.

## Get Central League First Base Fielding Stats
`get_central_1b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get first base fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_1b_fielding_stats

# Get central league first base fielding stats for the 2001 season
first_base_fielding = get_central_1b_fielding_stats(2001)
```

## Get Pacific League First Base Fielding Stats
`get_pacific_1b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get first base fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_1b_fielding_stats

# Get pacific league first base fielding stats for the most recent season
first_base_fielding = get_pacific_1b_fielding_stats()

```

## Get All First Base Fielding Stats
`get_1b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all first base fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_1b_fielding_stats

# Get first base fielding stats for the 2023 season
first_base_fielding = get_1b_fielding_stats(2023)

```

## Get First Base Fielding Stats by Team
`get_1b_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get first base fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_1b_fielding_stats_by_team

# Get most recent first base fielding stats for the Chunichi Dragons
first_base_fielding = get_1b_fielding_stats_by_team("Chunichi Dragons")

```

## Get Central League Second Base Fielding Stats
`get_central_2b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get second base fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_2b_fielding_stats

# Get central league second base fielding stats for the 2011 season
second_base_fielding = get_central_2b_fielding_stats(2011)
```

## Get Pacific League Second Base Fielding Stats
`get_pacific_2b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get second base fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_2b_fielding_stats

# Get pacific league second base fielding stats for the 2020 season
second_base_fielding = get_pacific_2b_fielding_stats(2020)

```

## Get All Second Base Fielding Stats
`get_2b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all second base fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_2b_fielding_stats

# Get second base fielding stats for the 1969 season
second_base_fielding = get_2b_fielding_stats(1969)

```

## Get Second Base Fielding Stats by Team
`get_2b_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get second base fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_2b_fielding_stats_by_team

# Get most recent second base fielding stats for the Chunichi Dragons
second_base_fielding = get_2b_fielding_stats_by_team("Chunichi Dragons")

```

## Get Central League Third Base Fielding Stats
`get_central_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get third base fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_3b_fielding_stats

# Get central league third base fielding stats for the 2019 season
third_base_fielding = get_central_2b_fielding_stats(2019)
```

## Get Pacific League Third Base Fielding Stats
`get_pacific_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get third base fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_3b_fielding_stats

# Get pacific league third base fielding stats for the 2001 season
third_base_fielding = get_pacific_3b_fielding_stats(2001)

```

## Get All Third Base Fielding Stats
`get_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all third base fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_3b_fielding_stats

# Get third base fielding stats for the 1954 season
third_base_fielding = get_3b_fielding_stats(1954)

```

## Get Third Base Fielding Stats by Team
`get_3b_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get third base fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_3b_fielding_stats_by_team

# Get 2019 third base fielding stats for the Chunichi Dragons
third_base_fielding = get_3b_fielding_stats_by_team("Chunichi Dragons", 2019)

```

## Get Central League Shortstop Fielding Stats
`get_central_ss_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get shortstop fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_ss_fielding_stats

# Get central league shortstop fielding stats for the 2015 season
shortstop_fielding = get_central_ss_fielding_stats(2015)
```

## Get Pacific League Shortstop Fielding Stats
`get_pacific_ss_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get shortstop fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_ss_fielding_stats

# Get pacific league shortstop fielding stats for the 2009 season
shortstop_fielding = get_pacific_ss_fielding_stats(2009)

```

## Get All Shortstop Fielding Stats
`get_3b_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all shortstop fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_ss_fielding_stats

# Get shortstop fielding stats for the 1976 season
shortstop_fielding = get_ss_fielding_stats(1976)

```

## Get Shortstop Fielding Stats by Team
`get_ss_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get shortstop fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_ss_fielding_stats_by_team

# Get 2017 shortstop base fielding stats for the Hiroshima Carp
shortstop_fielding = get_ss_fielding_stats_by_team("Hiroshima Carp", 2017)

```

## Get Central League Outfield Fielding Stats
`get_central_of_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get outfield fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_of_fielding_stats

# Get central league outfield fielding stats for the 2018 season
outfield_fielding = get_central_of_fielding_stats(2018)
```

## Get Pacific League Outfield Fielding Stats
`get_pacific_of_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get outfield fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_of_fielding_stats

# Get pacific league outfield fielding stats for the 2024 season
outfield_fielding = get_pacific_of_fielding_stats(2024)

```

## Get All Outfield Fielding Stats
`get_of_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all outfield fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_of_fielding_stats

# Get outfield fielding stats for the 1976 season
outfield_fielding = get_of_fielding_stats(1976)

```

## Get Outfield Fielding Stats by Team
`get_of_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get outfield fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_of_fielding_stats_by_team

# Get 2017 outfield fielding stats for the Nippon Ham Fighters
outfield_fielding = get_of_fielding_stats_by_team("Nippon Ham Fighters", 2017)

```

## Get Central League Pitcher Fielding Stats
`get_central_p_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get pitcher fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_p_fielding_stats

# Get central league pitcher fielding stats for the 2017 season
pitcher_fielding = get_central_p_fielding_stats(2017)
```

## Get Pacific League Pitcher Fielding Stats
`get_pacific_p_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get pitcher fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_p_fielding_stats

# Get pacific league pitcher fielding stats for the 2023 season
pitcher_fielding = get_pacific_p_fielding_stats(2023)

```

## Get All Pitcher Fielding Stats
`get_p_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all pitcher fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_p_fielding_stats

# Get outfield fielding stats for the 1986 season
pitcher_fielding = get_p_fielding_stats(1986)

```

## Get Pitcher Fielding Stats by Team
`get_p_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get pitcher fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_p_fielding_stats_by_team

# Get 2019 pitcher fielding stats for the Yakult Swallows
pitcher_fielding = get_p_fielding_stats_by_team("Yakult Swallows", 2019)

```

## Get Central League Catcher Fielding Stats
`get_central_c_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get catcher fielding stats for the central league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_c_fielding_stats

# Get central league catcher fielding stats for the 2017 season
catcher_fielding = get_central_c_fielding_stats(2017)
```

## Get Pacific League Catcher Fielding Stats
`get_pacific_c_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get catcher fielding stats for the pacific league.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_c_fielding_stats

# Get pacific league catcher fielding stats for the 2021 season
catcher_fielding = get_pacific_c_fielding_stats(2021)

```

## Get All Catcher Fielding Stats
`get_c_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all catcher fielding stats.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_c_fielding_stats

# Get catcher fielding stats for the 1999 season
catcher_fielding = get_c_fielding_stats(1999)

```

## Get Catcher Fielding Stats by Team
`get_c_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get catcher fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_c_fielding_stats_by_team

# Get 2018 catcher fielding stats for the Yakult Swallows
catcher_fielding = get_c_fielding_stats_by_team("Yakult Swallows", 2018)

```

# Get All Fielding Stats
`get_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all fielding stats for the year entered.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_fielding_stats

# Get all fielding stats from 2019
all_fielding_stats = get_fielding_stats(2019)

```

## Get All Fielding Stats by Team
`get_fielding_stats_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get all fielding stats for a specific team.

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_fielding_stats_by_team

# Get 2018 fielding stats for the Yakult Swallows
yakult_fielding-stats = get_fielding_stats_by_team("Yakult Swallows", 2018)

```

# Get All Pacific League Fielding Stats Stats
`get_pacific_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all pacific league fielding stats for the year entered.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_pacific_fielding_stats

# Get all pacific league fielding stats from 2019
all_fielding_stats = get_pacific_fielding_stats(2024)

```

# Get All Central League Fielding Stats Stats
`get_central_fielding_stats(year: Optional[int] = None) -> pd.DataFrame`

This function will get all central league fielding stats for the year entered.

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.fielding_stats import get_central_fielding_stats

# Get all central league fielding stats from the most recent season
all_fielding_stats = get_central_fielding_stats()

```