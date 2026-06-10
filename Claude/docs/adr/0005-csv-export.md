# 5. CSV Export Format

Date: 2026-05-21

## Status

Accepted

## Context

The requirements specify that the dashboard must support an export feature, allowing either an HTML/PDF report or a CSV containing KPIs.

## Decision

We will implement the export feature as a CSV download containing the aggregated KPIs and cleaned data.

## Consequences

*   **Positive:** Simple, robust, and fast to implement. Avoids the complexity and external dependencies required for backend PDF generation.
*   **Negative:** Less visually appealing than a formatted PDF report.
