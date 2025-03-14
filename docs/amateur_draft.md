# Amateur Draft

This group of functions gets data for the NPB amateur draft.

## Get DraftRresults
`get_draft_results(year: Optional[int] = None) -> dict`

The function will return a dict with pandas dataframe with the amateur draft results from the year entered. The identifier will be the draft round names

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.amateur_draft import get_draft_results

# Get amateur draft results for the most recent season
draftResults = get_draft_results()

# Get amateur draft results for the 2022 season
draftResults = get_draft_results(2022)

```

## Get Round Results
`get_round_results(round: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get NPB amateur draft results for the round entered

### Arguments
`round: ` A string value representing the round of the draft for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries
```python
from pynpb.amateur_draft import get_draft_results

# Get first round initial picks results for the most recent season
draftResults = get_draft_results("First Round - initial picks")

```

## Get Draft Results by Team
`get_draft_results_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame`

This function will get NPB amateur draft results for the round entered

### Arguments
`team: ` A string value representing the NPB team for which to retrieve data.

`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.amateur_draft import get_draft_results_by_team

# Get 2018 draft results for the Seibu Lions
draftResults = get_draft_results_by_team("Seibu Lions", 2018)
```