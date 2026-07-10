# 2. Tech Stack: React and Python (FastAPI)

Date: 2026-05-21

## Status

Accepted

## Context

We need to choose a technology stack for the client-server architecture. The application must handle CSV uploads, perform data cleaning (handling nulls, invalid dates, decimal separators), and aggregate data to generate KPIs and charts.

## Decision

We will use React (TypeScript) for the frontend and Python (FastAPI) with SQLite for the backend.

## Consequences

*   **Positive:** Python's data ecosystem (Pandas) will drastically simplify the required data cleaning and CSV parsing compared to Node.js.
*   **Positive:** React has a rich ecosystem of charting libraries (e.g., Recharts) for the dashboard requirements.
*   **Negative:** Requires the development team to be familiar with two different languages (TypeScript and Python).
