## What to build

The second half of the data ingestion process: column mapping and data cleaning.

After previewing the CSV, the user must be prompted to explicitly map their CSV columns to the system's required roles: "Date", "Category", and "Value". The backend will receive this mapping, use Pandas to parse the full dataset, and apply our strict data cleaning policy: any row missing a valid mapped Date, Category, or Value must be dropped entirely. The cleaned dataset is then saved for analytics.

## Acceptance criteria

- [ ] Frontend provides dropdowns for the user to assign CSV columns to Date, Category, and Value roles.
- [ ] Backend endpoint accepts the column mapping configuration.
- [ ] Backend parses the CSV using Pandas and validates the chosen columns.
- [ ] Backend applies the strict dropping policy for any row with invalid or empty mapped data.
- [ ] Backend stores the cleaned, normalized dataset.
- [ ] Frontend transitions to a loading state or placeholder dashboard upon successful mapping.

## Blocked by

- #2 (002-csv-upload-and-preview.md)
