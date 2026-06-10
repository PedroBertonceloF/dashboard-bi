## What to build

The first half of the data ingestion process: allowing an authenticated user to upload a CSV file and view a raw preview of the data. 

This involves creating the `datasets` database schema to track uploaded files. The frontend requires a file upload component. The backend must provide an endpoint to receive the raw CSV file, store it temporarily or permanently associated with the user, and return the first few rows as a JSON payload for the frontend to render as a preview table.

## Acceptance criteria

- [ ] Database schema includes a `datasets` table linked to `users`.
- [ ] Frontend provides an upload interface that accepts `.csv` files.
- [ ] Backend endpoint successfully receives and stores the uploaded CSV.
- [ ] Backend endpoint parses the first ~5 rows of the CSV and returns them.
- [ ] Frontend displays the returned rows as a preview table to the user.

## Blocked by

- #1 (001-authentication-system.md)
