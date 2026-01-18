# Alembic Migrations

This directory contains database migration scripts.

## Usage

### Initialize migrations (first time only)
```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
```

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

### Show current revision
```bash
alembic current
```

### Show migration history
```bash
alembic history
```
