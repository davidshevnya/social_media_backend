# Social Media Backend API

A practice project I built while learning Flask and backend development. This is a RESTful API for a social media platform with users and posts.

## About This Project

This is a learning project where I explored backend development with Flask. It's not production-ready, but it helped me understand the fundamentals of building APIs and working with databases.

## Features

- User model with basic CRUD operations
- Post model with basic CRUD operations
- JWT authentication
- RESTful API endpoints
- Database integration with SQLAlchemy
- Database migrations with Alembic
- API testing with pytest

## Tech Stack

- **Flask** - Python web framework
- **Flask-SQLAlchemy-Lite** - Database ORM
- **Flask-Marshmallow** - Object serialization/deserialization
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Alembic** - Database migrations
- **PostgreSQL** - Database (with psycopg2)
- **pytest** - Testing framework
- **uv** - Fast Python package installer

## Installation

1. Clone the repository:
```bash
git clone https://github.com/justdawy/social_media_backend.git
cd social_media_backend
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Configure the application:
```bash
# Edit app/config.py with your database credentials and secret keys
# Set DATABASE_URI, JWT_SECRET_KEY, etc.
```

4. Set up the database:
```bash
# Make sure PostgreSQL is running
uv run flask db upgrade
```

5. Run the application:
```bash
uv run run.py
```

## Running Tests
```bash
uv run pytest
```

## What I Learned

This project was a great hands-on introduction to backend development. Here's what I learned:

- **RESTful API Design** - Understanding HTTP methods (GET, POST, PUT, DELETE) and how to structure endpoints logically
- **Database Modeling** - Creating relationships between User and Post models using SQLAlchemy ORM
- **Flask Framework** - Working with Flask's routing system, request handling, and response formatting
- **API Development** - Handling JSON data, status codes, and error responses
- **Authentication** - Implementing JWT-based authentication for secure endpoints
- **Data Serialization** - Using Marshmallow schemas to validate and serialize data
- **Database Migrations** - Managing database schema changes with Alembic
- **Testing** - Writing tests for API endpoints with pytest
- **Configuration Management** - Separating config from code for different environments
- **Project Structure** - Organizing a Flask application with models, routes, and configurations
- **Modern Python Tooling** - Using uv for fast dependency management
- **Version Control** - Using Git and GitHub for code management and collaboration

## Next Steps

If I continue working on this, I'd like to add:
- More complex relationships (comments, likes, followers)
- API documentation with Swagger/OpenAPI
- Password reset functionality
- Rate limiting

---

*This is a learning project and may contain bugs or incomplete features. Feel free to explore the code!*