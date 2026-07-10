# 1. Client-Server Architecture with Authentication

Date: 2026-05-21

## Status

Accepted

## Context

The assignment problem (WEB-02) calls for a simple CSV upload and BI dashboard. A pure frontend application (e.g., React parsing CSV in the browser) would suffice to meet the core functional requirements. However, the assignment's global grading rubric includes a strict security checklist requiring "Senhas com hash e salt", "tokens com expiração", "controle de acesso", and "proteção contra SQL injection". 

## Decision

We will implement a client-server architecture with a dedicated backend, a database, and a user authentication system.

## Consequences

*   **Positive:** Guarantees that the project can be evaluated against and score points for all items on the assignment's security checklist.
*   **Negative:** Significantly increases the scope and complexity of the project compared to a pure frontend solution. We must now manage state, database migrations, and authentication flows.
