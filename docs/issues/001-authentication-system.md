## What to build

End-to-end authentication system to satisfy the strict security grading criteria. This slice cuts through the database schema, backend API, and frontend UI. It includes setting up the basic React and FastAPI project structures.

We need a database schema for `users`. The FastAPI backend must provide endpoints for user registration and login, utilizing bcrypt for password hashing and generating short-lived JWTs. The React frontend needs pages for Login and Registration, and an authentication context to manage the user's session token and protect the application routes.

## Acceptance criteria

- [ ] FastAPI backend project is initialized.
- [ ] React (TypeScript) frontend project is initialized.
- [ ] Database schema includes a `users` table with hashed passwords.
- [ ] Registration endpoint successfully creates a new user.
- [ ] Login endpoint validates credentials and returns a valid JWT.
- [ ] Frontend has functioning Login and Registration views.
- [ ] Frontend successfully stores the token and can restrict access to a placeholder protected route.

## Blocked by

None - can start immediately
