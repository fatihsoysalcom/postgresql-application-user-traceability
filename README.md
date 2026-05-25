# PostgreSQL Application User Traceability

This example demonstrates how to achieve real application user traceability in PostgreSQL, addressing a common limitation where role-based audit logging (like pgAudit) might obscure the actual user initiating an action. It shows how to set the `application_name` session variable before performing database operations, allowing for better identification of who did what, which is crucial for compliance standards like GDPR.

## Language

`python`

## How to Run

1. Ensure you have PostgreSQL running and `psycopg2` installed (`pip install psycopg2-binary`).
2. Set the following environment variables for your PostgreSQL connection: `PG_DB_NAME`, `PG_DB_USER`, `PG_DB_PASSWORD`, `PG_DB_HOST` (optional, default `localhost`), `PG_DB_PORT` (optional, default `5432`).
3. Run the script: `python main.py`

## Original Article

This example accompanies the Turkish article: [pgAudit Yetkilendirme Açığı: GDPR Uyumunda Rol Bazlı Günlüklemenin Yetmezliği](https://fatihsoysal.com/blog/pgaudit-yetkilendirme-acigi-gdpr-uyumunda-rol-bazli-gunluklemenin-yetmezligi/).

## License

MIT — see [LICENSE](LICENSE).
