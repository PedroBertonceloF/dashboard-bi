# 3. Two-Step CSV Upload Wizard

Date: 2026-05-21

## Status

Accepted

## Context

The application needs to generate specific visualizations (time-series, category bar chart) and KPIs from arbitrary user-uploaded CSVs. To do this, the system must understand the semantic meaning of the CSV columns.

## Decision

We will implement a 2-step wizard for data ingestion:
1.  **Upload & Mapping:** The user uploads a CSV, sees a preview, and explicitly maps their columns to the system's required roles (Date, Category, Value).
2.  **Dashboard:** The system processes the data based on the mapping and displays the dashboard.

## Consequences

*   **Positive:** Guarantees the backend has the correct semantic data to generate charts without relying on error-prone auto-detection.
*   **Positive:** Provides a clear mental model for the user.
*   **Negative:** Adds an extra step to the user journey before they see value (the dashboard).
