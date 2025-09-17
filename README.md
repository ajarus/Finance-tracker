# 🏦 Personal Finance Tracker API

A modern, scalable REST API for personal finance management built with FastAPI, PostgreSQL, and Docker.

## 🚀 Features

- **User Authentication** - JWT-based secure authentication
- **Transaction Management** - CRUD operations for income/expense tracking
- **Financial Analytics** - Category-based spending analysis and reports
- **RESTful API** - Clean, well-documented API endpoints
- **Database Migrations** - Alembic for schema versioning
- **Dockerized** - Easy deployment with Docker Compose
- **CI/CD** - GitHub Actions for automated testing and deployment

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2
- **Containerization**: Docker & Docker Compose
- **Migrations**: Alembic
- **Testing**: Pytest with async support
- **CI/CD**: GitHub Actions
- **Code Quality**: Black, isort, flake8, mypy

## 📦 Installation

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (optional, Docker provided)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ajarus/finance-tracker.git
   cd finance-tracker