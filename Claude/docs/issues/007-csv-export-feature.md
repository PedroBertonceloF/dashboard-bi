## What to build

The export feature allowing users to download their processed data.

The frontend needs an "Export" button on the Dashboard. The backend must provide an endpoint that receives the currently applied filters and generates a CSV file. This CSV must contain the calculated KPIs and the underlying aggregated data used to power the current view of the charts.

## Acceptance criteria

- [ ] Frontend Dashboard includes an "Export to CSV" button.
- [ ] Backend provides an endpoint that returns a properly formatted `text/csv` response.
- [ ] The generated CSV includes the high-level KPIs.
- [ ] The generated CSV includes the filtered, aggregated data.
- [ ] Clicking the frontend button triggers a browser file download of the CSV.

## Blocked by

- #6 (006-interactive-dashboard-filtering.md)
