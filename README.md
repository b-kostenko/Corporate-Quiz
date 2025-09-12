# Corporate Quiz Management System

A comprehensive FastAPI-based application designed for companies to manage and conduct quizzes for employee skill development and assessment. This system enables organizations to create, distribute, and track quiz performance across their teams, fostering continuous learning and professional development.

## Project Overview

The Corporate Quiz Management System is a modern web application that facilitates:

- **Employee Skill Assessment**: Regular quiz administration to evaluate and improve employee competencies
- **Company-wide Learning**: Structured knowledge testing across different departments and roles
- **Performance Tracking**: Comprehensive analytics on quiz completion rates and scores
- **Role-based Access Control**: Secure management of quiz content and company data
- **Scalable Architecture**: Built with enterprise-grade technologies for reliability and performance

## Key Features

### Company Management
- **Multi-company Support**: Each company operates independently with its own quiz ecosystem
- **Role-based Permissions**: Three-tier access system (Owner, Admin, Member)
- **Company Invitations**: Streamlined process for adding new team members
- **Company Profiles**: Comprehensive company information management with logos and descriptions

### Quiz System
- **Dynamic Quiz Creation**: Create quizzes with multiple questions and answer options
- **Flexible Question Types**: Support for various question formats and correct answer validation
- **Quiz Attempts Tracking**: Monitor individual and company-wide quiz performance
- **Score Calculation**: Automatic scoring with detailed performance metrics
- **Quiz Management**: Full CRUD operations for quiz content management

### User Management
- **Secure Authentication**: JWT-based authentication with refresh token support
- **User Profiles**: Personal information management with avatar support
- **Password Security**: Bcrypt hashing for secure password storage
- **Email Validation**: Robust email verification and validation

### Analytics & Reporting
- **Performance Metrics**: Track quiz completion rates, scores, and improvement over time
- **Company Statistics**: Aggregate data for organizational insights
- **Individual Progress**: Personal performance tracking for employees

### Technical Features
- **Async/Await Support**: High-performance asynchronous operations
- **Database Migrations**: Alembic-powered schema management
- **Background Tasks**: Celery integration for scheduled operations
- **File Storage**: Local file storage system for media assets
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.12+**: Latest Python features and performance improvements

### Database & ORM
- **PostgreSQL**: Robust relational database for data persistence
- **SQLAlchemy 2.0**: Modern async ORM with type safety
- **Alembic**: Database migration management

### Authentication & Security
- **JWT (PyJWT)**: Secure token-based authentication
- **Bcrypt**: Password hashing and verification
- **Pydantic**: Data validation and serialization

### Task Queue & Caching
- **Celery**: Distributed task queue for background processing
- **Redis**: Message broker and caching layer

### Development Tools
- **Ruff**: Fast Python linter and formatter
- **Poetry**: Dependency management and packaging
- **Docker**: Containerization for consistent deployment

## Installation & Setup

### Prerequisites

Before running the application, ensure you have the following installed:

- **Docker & Docker Compose**: For containerized deployment
- **Python 3.12+**: If running locally without Docker
- **Poetry**: For Python dependency management (if running locally)

### Environment Configuration

1. **Clone the repository**:
   ```bash
   git clone https://github.com/b-kostenko/Corporate-Quiz.git
   cd Corporate-Quiz
   ```

2. **Create environment file**:
   ```bash
   cp env.example .env
   ```

3. **Configure environment variables** in `.env`:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/dbname
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432

   # JWT Settings
   JWT_SECRET_KEY=your-super-secret-jwt-key
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   JWT_REFRESH_TOKEN_EXPIRE_MINUTES=10080 # 1 day
   JWT_TOKEN_TYPE=bearer

   # Celery Settings
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0

   # Storage Settings
   STORAGE_BASE_PATH=./media
   STORAGE_BASE_URL=http://localhost:8000/media
   STORAGE_ALLOWED_EXTENSIONS='[".jpg", ".jpeg", ".png", ".gif", ".webp"]'
   STORAGE_MAX_FILE_SIZE=10485760
   ```

### Docker Deployment (Recommended)

1. **Build and start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - **API Documentation**: http://localhost:8000/docs
   - **Application**: http://localhost:8000
   - **Database**: localhost:5432
   - **Redis**: localhost:6379

## API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /auth/refresh` - Token refresh

### Company Management
- `POST /companies` - Create new company
- `GET /companies` - List user's companies
- `PUT /companies/{company_id}` - Update company
- `DELETE /companies/{company_id}` - Delete company
- `POST /companies/{company_id}/invite` - Invite user to company
- `POST /companies/invitations/{invitation_id}/accept` - Accept invitation

### Quiz Management
- `POST /quizzes/{company_id}` - Create quiz
- `GET /quizzes/{company_id}` - List company quizzes
- `PUT /quizzes/{quiz_id}/{company_id}` - Update quiz
- `DELETE /quizzes/{quiz_id}/{company_id}` - Delete quiz
- `POST /quizzes/{quiz_id}/{company_id}/attempts` - Attempt quiz

### User Management
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `POST /users/upload-avatar` - Upload user avatar

## Project Structure

```
app/
├── application/          # API layer
│   └── api/              # Route handlers and endpoints
├── core/                 # Business logic layer
│   ├── interfaces/       # Repository and service interfaces
│   ├── repositories/     # Data access layer
│   ├── schemas/          # Pydantic models
│   └── services/         # Business logic services
├── infrastructure/       # Infrastructure layer
│   ├── celery/           # Background task configuration
│   ├── migrations/       # Database migrations
│   ├── postgres/         # Database models and connection
│   ├── security/         # Authentication and security
│   └── storage/          # File storage implementation
├── utils/                # Utility functions and exceptions
└── settings.py           # Application configuration
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Role-based Access Control**: Granular permissions system
- **Input Validation**: Pydantic models for data validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Configuration**: Configurable cross-origin resource sharing

## Performance & Scalability

- **Async/Await**: Non-blocking I/O operations
- **Connection Pooling**: Efficient database connection management
- **Background Tasks**: Celery for long-running operations
- **Caching**: Redis for session and data caching
- **Database Indexing**: Optimized queries with proper indexing

## Development

### Code Quality
```bash
# Format code
ruff format

# Lint code
ruff check

# Fix linting issues
ruff check --fix

# Check specific file
ruff check app/core/services/quiz_service.py

# Format specific directory
ruff format app/
```

### Database Operations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact: bogdankostenko83@gmail.com

---

**Built with ❤️ using FastAPI, PostgreSQL, and modern Python practices**