# GLPI Reports

![GLPI Reports](https://img.shields.io/badge/GLPI-Reports-blue)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange)

A modern, clean architecture service for managing device reports with event-driven design.

## 🚀 Features

- **Device Report Management**: Create, update, retrieve, and delete device reports
- **Event-Driven Design**: Outbox pattern for reliable event publishing
- **API Documentation**: Auto-generated OpenAPI documentation
- **Background Processing**: Scheduled tasks with Hatchet SDK
- **Database Migrations**: Managed through Alembic

## 📋 Requirements

- Python 3.12+
- PostgreSQL
- RabbitMQ
- Docker (optional)

## 🛠️ Installation

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/glpi-reports.git
cd glpi-reports

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## ⚙️ Configuration

The application uses environment variables for configuration:

### Database Configuration
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=reports
```

### RabbitMQ Configuration
```
RABBIT_HOST=localhost
RABBIT_PORT=5672
RABBIT_USER=guest
RABBIT_PASSWORD=guest
```

### Server Configuration
```
UVICORN_SERVER_HOST=0.0.0.0
UVICORN_SERVER_PORT=8000
```

### Hatchet Configuration
```
HATCHET_API_KEY=your_api_key
```

## 🚀 Usage

### Using Just Commands

The project includes a `justfile` for common development tasks. [Just](https://github.com/casey/just) is a handy command runner that helps simplify project workflows.

#### Prerequisites

- [Just](https://github.com/casey/just) command runner
- [uv](https://github.com/astral-sh/uv) Python package manager
- [Cargo/Rust](https://www.rust-lang.org/tools/install) (for running helper scripts)

#### Available Commands

```bash
# Install dependencies
just install

# Run linting
just lint

# Run tests (starts test containers, runs tests, then stops containers)
just tests

# Start the application (with Docker)
just run-app

# Stop the application
just stop-app
```

The justfile uses Rust helper scripts in the `scripts/src/` directory to:
- Load environment variables from `.env.dev` or `.env.test`
- Manage Docker containers with appropriate compose files
- Run tests with proper setup and teardown

### Running the API Server Manually

```bash
# Run database migrations
reports upgrade-migration

# Start the API server
reports start-uvicorn
```

### Running the Worker Manually

```bash
# Start the background worker
reports start-worker
```

### API Endpoints

- `GET /reports`: List all reports
- `GET /reports/{report_id}`: Get a specific report
- `POST /reports/`: Create a new report
- `PUT /reports/{report_id}`: Update a report
- `DELETE /reports/{report_id}`: Delete a report
- `GET /healthcheck`: Check service health

### Key Components

- **Event Bus**: For handling domain events
- **Outbox Pattern**: For reliable event publishing
- **Unit of Work**: For transaction management
- **Command/Query Handlers**: For processing requests

## 🧪 Testing

```bash
# Run tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
