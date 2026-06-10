## What to build

The visual components of the Dashboard: the time-series line chart and the categorical bar chart.

The backend analytics module must be extended to aggregate the cleaned data by the mapped "Date" column (for the time-series) and the mapped "Category" column (for the bar chart). The frontend will integrate a charting library (e.g., Recharts) to render this aggregated data on the Dashboard view alongside the KPIs.

## Acceptance criteria

- [ ] Backend analytics module aggregates data correctly for a time-series (Value over Date).
- [ ] Backend analytics module aggregates data correctly for categories (Value by Category).
- [ ] Backend endpoint exposes this aggregated chart data.
- [ ] Frontend integrates a charting library.
- [ ] Frontend successfully renders a time-series line chart.
- [ ] Frontend successfully renders a categorical bar chart.

## Blocked by

- #4 (004-core-kpi-generation.md)
