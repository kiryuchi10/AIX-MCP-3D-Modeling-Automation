# MCP 3D Modeling Automation - Backend

FastAPI backend with Blender integration for automated 3D modeling from images and drawings.

## Features

- **Project Management**: Organize work by projects
- **Asset Upload**: Upload images, 2D drawings, or 3D models
- **Dimension Extraction**: Extract dimensions from scale references
- **Script Generation**: Generate Blender Python scripts from extracted dimensions
- **Blender Integration**: Execute Blender scripts headlessly (optional)
- **Job Queue**: Async task processing with Redis Queue (RQ)
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations

## Setup

### 1. Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql+psycopg2://mcp_user:mcp_password@localhost:5432/mcp3d

# Redis Queue
REDIS_URL=redis://localhost:6379/0
RQ_QUEUE_NAME=default

# Storage
LOCAL_UPLOAD_DIR=./uploads
LOCAL_OUTPUT_DIR=./outputs

# Blender Integration
BLENDER_EXEC_MODE=local_only  # or server_headless
BLENDER_PATH=/usr/bin/blender
BLENDER_WORKDIR=./outputs

# Security
SECRET_KEY=your-secret-key-here
```

### 2. Database Setup

```bash
# Create database
createdb mcp3d

# Or with PostgreSQL client
psql -U postgres
CREATE DATABASE mcp3d;
CREATE USER mcp_user WITH PASSWORD 'mcp_password';
GRANT ALL PRIVILEGES ON DATABASE mcp3d TO mcp_user;
```

### 3. Run Migrations

```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Install Dependencies

```bash
cd backend/app
pip install -r requirements.txt
```

**Note**: The existing `requirements.txt` already includes most dependencies. You may need to add:
- `rq` for Redis Queue
- `pydantic-settings` (may already be included)

```bash
pip install rq pydantic-settings
```

### 5. Run Services

#### Terminal 1: Redis (if not running)
```bash
redis-server
```

#### Terminal 2: RQ Worker
```bash
cd backend
rq worker default
```

#### Terminal 3: FastAPI Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Health check
- `GET /` - API info

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project

### Assets
- `POST /api/v1/assets/upload` - Upload files
- `GET /api/v1/assets/{id}` - Get asset info
- `GET /api/v1/assets/{id}/download` - Download file
- `GET /api/v1/assets/{id}/preview` - Preview file

### Extraction
- `POST /api/v1/extraction/scale-reference` - Set scale reference
- `GET /api/v1/extraction/result/{project_id}` - Get extraction result

### Scripts
- `GET /api/v1/scripts/{project_id}` - List script versions
- `GET /api/v1/scripts/{project_id}/latest` - Get latest script text
- `GET /api/v1/scripts/{script_id}/download` - Download script file

### Jobs
- `POST /api/v1/jobs` - Create job (extract/generate_script/run_blender)
- `GET /api/v1/jobs/{id}` - Get job status
- `GET /api/v1/jobs` - List jobs (with filters)

### Blender
- `POST /api/v1/blender/smoke` - Smoke test for Blender integration

## Workflow

1. **Create Project**: `POST /api/v1/projects`
2. **Upload Assets**: `POST /api/v1/assets/upload` (images, drawings, 3D files)
3. **Set Scale Reference**: `POST /api/v1/extraction/scale-reference`
4. **Extract Dimensions**: `POST /api/v1/jobs` with `job_type="extract"`
5. **Generate Script**: `POST /api/v1/jobs` with `job_type="generate_script"`
6. **Run Blender** (optional): `POST /api/v1/jobs` with `job_type="run_blender"`

## Blender Integration

### Modes

#### Local Only (Default)
- Server generates scripts only
- User runs Blender locally: `blender -b -P script.py`
- Recommended for development/testing

#### Server Headless
- Server runs Blender in headless mode
- Requires Blender installed on server
- Set `BLENDER_EXEC_MODE=server_headless` in `.env`

### Smoke Test

Test Blender integration:

```bash
curl -X POST http://localhost:8000/api/v1/blender/smoke
```

Should return:
```json
{
  "ok": true,
  "stl_exists": true,
  "stl_path": "./outputs/smoke_test/smoke_cube.stl"
}
```

## Database Schema

### Models

- **Project**: Container for assets, extractions, scripts
- **Asset**: Uploaded files (images, drawings, 3D models)
- **ScaleReference**: Calibration dimension for extraction
- **ExtractionResult**: Extracted dimensions, features, tasks (versioned)
- **ScriptVersion**: Generated Blender Python scripts (versioned)
- **Job**: Async task tracking (extract, generate_script, run_blender)

### Relationships

- Project → Assets (1:N)
- Project → ScaleReference (1:1, latest used)
- Project → ExtractionResults (1:N, versioned)
- Project → ScriptVersions (1:N, versioned)
- Project → Jobs (1:N)

## Development

### Running Tests

```bash
pytest
```

### Code Style

```bash
black app/
isort app/
```

### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Troubleshooting

### Blender Not Found
- Check `BLENDER_PATH` in `.env`
- Verify Blender is installed: `blender --version`
- Windows: Use full path: `C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe`

### Job Stuck in Queued
- Ensure RQ worker is running: `rq worker default`
- Check Redis connection: `redis-cli ping`

### Database Connection Error
- Verify `DATABASE_URL` format: `postgresql+psycopg2://user:pass@host:port/db`
- Ensure PostgreSQL is running
- Check database exists and user has permissions

## License

[Your License Here]
