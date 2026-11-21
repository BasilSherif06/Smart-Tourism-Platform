# Smart Tourism Platform

An AI-powered tourism platform that helps users plan personalized trips and dynamically replan their itineraries when unexpected disruptions occur.

## Project Structure

```text
Smart-Tourism-Platform/
├── ai/                     # AI and LLM integration
├── backend/                # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── src/
│   │   ├── api/
│   │   ├── controllers/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   └── schemas/
│   ├── tests/
│   ├── .env.example
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
├── docs/                   # Project documentation
├── frontend/               # Frontend application
└── README.md
```

## Backend Setup

### Prerequisites

Before starting, install:

- Python 3.12
- Anaconda or Miniconda
- Docker Desktop
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/BasilSherif06/Smart-Tourism-Platform.git
cd Smart-Tourism-Platform
```

### 2. Create and Activate the Python Environment

```bash
conda create -n smart-tourism python=3.12 -y
conda activate smart-tourism
```

### 3. Install Dependencies

Navigate to the backend directory:

```bash
cd backend
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your local `.env` file using the example:

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your database credentials:

```env
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=smart_tourism
DB_USER=smart_tourism_user
DB_PASSWORD=your_private_password

APP_NAME=Smart Tourism Platform
APP_ENV=development
```

Use your own private database password.

**Note:** Port `5433` is used by default to avoid conflicts with PostgreSQL installations running directly on Windows. If that port is already occupied, choose another available host port and update `DB_PORT` accordingly.

Never commit your `.env` file to GitHub.

### 5. Start the PostgreSQL Database

Make sure Docker Desktop is running.

From the `backend` directory, execute:

```bash
docker compose up -d
```

This starts a PostgreSQL 16 container and creates your local database using the credentials configured in `.env`.

To verify that the container is running:

```bash
docker ps
```

To stop the database:

```bash
docker compose down
```

Your database data is persisted in a Docker volume, so stopping the container does not delete it.

### 6. Verify the Database Connection

Check the Alembic database connection:

```bash
alembic current
```

If the configuration is correct, Alembic should connect successfully to PostgreSQL.

### 7. Database Migrations

Database schema changes are managed using Alembic.

When migration files are available in the repository, apply them to your local database using:

```bash
alembic upgrade head
```

Migration files are shared through GitHub so that every developer can maintain the same database schema.

Each developer runs their own PostgreSQL container and database. Database records are local and are not automatically shared between developers.

## Important Notes

- Do not commit `.env` files or database credentials.
- Each developer must configure their own local database.
- Use Alembic migration files to share database schema changes.
- Do not delete Docker volumes unless you intentionally want to remove local database data.
- Keep your local branch synchronized with the team's `develop` branch.