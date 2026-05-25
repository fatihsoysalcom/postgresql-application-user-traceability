# postgresql-application-user-traceability
This example demonstrates how to achieve real application user traceability in PostgreSQL, addressing a common limitation where role-based audit logging (like pgAudit) might obscure the actual user initiating an action. It shows how to set the `application_name` session variable before performing database operations, allowing for better identificat
