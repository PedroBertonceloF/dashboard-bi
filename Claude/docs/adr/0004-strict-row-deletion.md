# 4. Strict Row Deletion for Data Cleaning

Date: 2026-05-21

## Status

Accepted

## Context

The system must clean the uploaded CSV data ("tratar vazios, datas inválidas") without inventing numbers. We must decide how to handle rows with partial validity (e.g., a valid Category but missing Date).

## Decision

We will adopt a strict dropping policy. If any row contains an invalid, empty, or unparseable value in the user-mapped Date, Category, or Value columns, the entire row will be dropped during processing.

## Consequences

*   **Positive:** Ensures total consistency. The sum of Values in the time-series will exactly match the sum of Values in the category bar chart.
*   **Negative:** Users might wonder why their total count is lower than expected if their CSV has many partially malformed rows. We must provide clear messaging about dropped rows.
