## What to build

Interactive filtering controls for the Dashboard.

The frontend must provide UI elements to filter the data by a specific Date range and by selecting one or more Categories. When filters are applied, the frontend must request updated data from the backend. The backend analytics module must dynamically apply these filters to the dataset before recalculating the KPIs and chart aggregations.

## Acceptance criteria

- [ ] Frontend provides a date range picker UI.
- [ ] Frontend provides a multi-select dropdown for Categories.
- [ ] Backend analytics functions and endpoints accept optional filter parameters.
- [ ] Backend correctly filters the dataset before aggregation based on the parameters.
- [ ] Dashboard KPIs and Charts automatically update when frontend filters are changed.

## Blocked by

- #5 (005-dashboard-visualizations.md)
