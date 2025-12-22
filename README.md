# 💰 Expense Tracker API

A robust, production-ready RESTful API for tracking personal expenses, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## ✨ Features

- 🔐 **Secure Authentication**: JWT-based login and registration.
- 💸 **Expense Management**: Full CRUD operations for personal expenses.
- 📂 **Categories**: Organize expenses with custom categories.
- 📊 **Insightful Summaries**: Monthly, daily, and category-wise spending reports.
- 📈 **Dashboard**: Holistic view of your financial health.
- 🐳 **Docker Ready**: Easy deployment with Docker and Docker Compose.
- 🔄 **Database Migrations**: Managed by Alembic.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Containerization**: [Docker](https://www.docker.com/)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized setup)
- PostgreSQL (if running locally)

### Running with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/expense-tracker-api.git
   cd expense-tracker-api
   ```

2. **Setup environment variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@db:5432/expense_db
   SECRET_KEY=your_super_secret_key
   ```

3. **Spin up the containers**:
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

### Local Development

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

- `POST /api/v1/auth/register`: Create a new account.
- `POST /api/v1/auth/login`: Authenticate and get a JWT token.
- `GET /api/v1/expenses`: List all expenses (paginated).
- `GET /api/v1/dashboard/`: Get a comprehensive spending overview.

---

## 🏗️ Architecture

For a detailed explanation of the project structure and design decisions, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
