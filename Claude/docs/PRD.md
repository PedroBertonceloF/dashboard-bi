# Product Requirements Document: WEB-02 BI Dashboard

## Problem Statement
The user needs to evaluate AI code generation tools by building a specific application (WEB-02) as part of a university assignment. The application requires users to upload CSV data and generate a BI dashboard with KPIs and visualizations. Furthermore, the assignment grading rubric mandates strict security implementations (authentication, hash/salt, token expiration) and thorough automated testing, which complicates a straightforward frontend-only CSV parser.

## Solution
We will build a Client-Server application using React (TypeScript) and Python (FastAPI). This architecture allows us to satisfy both the core functional requirements (CSV processing via Pandas, dashboard rendering) and the strict security criteria (dedicated auth system, JWTs). The data ingestion process will use a 2-step wizard to ensure accurate column mapping (Date, Category, Value) before generating the dashboard. Data cleaning will strictly drop malformed rows to ensure KPI and chart consistency without inventing data. Finally, users can export their processed data and KPIs as a CSV file.

## User Stories

1. As an unauthenticated user, I want to create an account with a secure password, so that I can access the system.
2. As a registered user, I want to log in using my credentials, so that I receive a temporary access token.
3. As a logged-in user, I want my session to expire after a set time, so that the system remains secure if I leave my computer.
4. As a user, I want to upload a CSV file, so that I can analyze my data.
5. As a user, I want to see a preview of my uploaded CSV, so that I can verify I uploaded the correct file.
6. As a user, I want to map specific columns from my CSV to "Date", "Category", and "Value" roles, so that the system knows how to aggregate the data.
7. As a user, I want the system to handle missing or invalid data by dropping the affected rows, so that my dashboard does not contain fabricated or inconsistent numbers.
8. As a user, I want to view a Dashboard containing key KPIs calculated from my Value column, so that I can understand high-level metrics.
9. As a user, I want to view a time-series chart based on my Date and Value columns, so that I can see trends over time.
10. As a user, I want to view a bar chart based on my Category and Value columns, so that I can compare different groups.
11. As a user, I want to filter the dashboard by a specific date range, so that I can narrow down my analysis.
12. As a user, I want to filter the dashboard by selecting multiple categories, so that I can compare specific groups.
13. As a user, I want the KPIs and charts to update dynamically when I apply filters, so that I can explore the data interactively.
14. As a user, I want to export the calculated KPIs and aggregated data as a CSV file, so that I can use the results outside the application.
15. As a grading evaluator, I want to see automated tests proving the corretude of the code, so that I can assign points according to the rubric.

## Implementation Decisions

- **Architecture:** Client-Server with Auth (React + FastAPI + SQLite). This fulfills the security grading criteria (ADR-0001, ADR-0002).
- **Backend Auth Module:** Will implement password hashing (bcrypt), salting, and short-lived JWT generation.
- **Data Ingestion Flow:** 2-step wizard in the frontend (Upload -> Map Columns -> View Dashboard) (ADR-0003).
- **Backend Ingestion Module:** Will utilize Pandas for robust CSV parsing and column validation.
- **Data Cleaning Policy:** Strict row dropping. Any row missing a valid mapped Date, Category, or Value will be discarded entirely (ADR-0004).
- **Backend Analytics Module:** A pure Python module that accepts a cleaned dataset and filter parameters, returning calculated KPIs and chart series data.
- **Export Format:** CSV export only, containing the KPIs and the underlying aggregated data used for the charts (ADR-0005).
- **Frontend State:** Will require context or state management for the User Session and the current Wizard step.
- **Database Schema:** Will include `users` (id, email, hashed_password) and `datasets` (id, user_id, raw_data_path or parsed_json_blob).

## Testing Decisions

- **Focus:** The primary focus for automated testing will be the **Backend Data Modules** (Ingestion and Analytics). These modules contain the core business logic of WEB-02.
- **Test Characteristics:** Good tests will provide raw CSV bytes (or mocked Pandas DataFrames) to the Analytics module and assert the correct KPI outputs and chart aggregations, rather than testing the internal Pandas methods.
- **Auth Testing:** Basic unit tests will verify password hashing and token generation in the Auth module to prove the security criteria are met.
- **Tooling:** Python `pytest` for backend testing.

## Out of Scope

- PDF generation for dashboard exports.
- Complex auto-detection of CSV columns (user must map them explicitly).
- Saving dashboards for later viewing (users upload a CSV, view the dashboard, and export; the CSV data is ephemeral or tied strictly to that session/upload).
- Password reset flows (basic login/register is sufficient for the security criteria).
- Advanced BI features like pivot tables or custom chart types.

## Further Notes

- The primary goal of this repository is to serve as a testbed for evaluating AI tools. The code should be kept as clean and modular as possible to facilitate this evaluation.
