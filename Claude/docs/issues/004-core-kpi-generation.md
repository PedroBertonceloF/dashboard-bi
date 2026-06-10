## What to build

The core analytics engine for generating top-level KPIs from the cleaned dataset. 

The backend requires a new, highly-testable analytics module that calculates aggregate metrics (e.g., Total Sum, Average) from the "Value" column. The frontend needs the main Dashboard view built out to fetch these KPIs from the backend and display them in styled metric cards. This slice includes the core automated tests for the analytics module, fulfilling the assignment's testing criteria.

## Acceptance criteria

- [ ] Backend analytics module includes a function to calculate total and average KPIs.
- [ ] Backend provides an endpoint to fetch these KPIs for a given dataset.
- [ ] Frontend Dashboard view successfully fetches and displays the KPIs.
- [ ] Automated unit tests (`pytest`) are written for the backend KPI calculation logic.
- [ ] Tests verify that KPI calculations are mathematically correct based on mocked inputs.

## Blocked by

- #3 (003-column-mapping-and-cleaning.md)
