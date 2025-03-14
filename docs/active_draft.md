# Active Draft

This group of functions gets data for the NPB active draft.

## Get Active Draft Results
`get_active_draft_results(year: Optional[int] = None) -> pd.DataFrame`

### Arguments
`year: ` An integer value representing the year for which to retrieve data. If not entered, results from most recent season will be retrieved.

#### Examples of Valid Queries

```python
from pynpb.active_draft import get_active_draft_results

# Get active draft results for the most recent season
draftResults = get_active_draft_results()

# Get acive draft results for the 2022 season
draftResults = get_active_draft_results(2022)

```
