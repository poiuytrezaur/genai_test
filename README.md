# Weather App

A production-ready weather application with user management and real-time weather data.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Weather App                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  HTML Templates          │  Static Assets                        │
│  • index.html            │  • CSS (style.css)                   │
│  • login.html            │  • JavaScript                        │
│  • register.html         │    - login.js                        │
│  • weather.html          │    - register.js                     │
│                          │    - weather.js                      │
└──────────────────┬──────────────────────────────────────────────┘
                   │ HTTP/HTTPS
                   │
┌──────────────────▼──────────────────────────────────────────────┐
│                       Flask Application                          │
├─────────────────────────────────────────────────────────────────┤
│  Routes Layer            │  Business Logic Layer                │
│  • auth_routes.py        │  • auth_service.py                   │
│    - /api/auth/register  │    - register_user()                 │
│    - /api/auth/login     │    - authenticate_user()             │
│    - /api/auth/logout    │    - get_user_by_id()                │
│    - /api/auth/me        │                                      │
│  • weather_routes.py     │  • weather_service.py                │
│    - /api/weather/current│    - get_weather()                   │
│                          │    - get_weather_description()       │
└──────────────────┬──────┴──────────────────┬───────────────────┘
                   │                          │
                   │                          │ HTTP
                   │                          │
┌──────────────────▼──────────────────────┐  │
│         Data Layer                      │  │
├─────────────────────────────────────────┤  │
│  database.py (SQLAlchemy)               │  │
│  • db initialization                    │  │
│                                         │  │
│  models/                                │  │
│  • user.py                              │  │
│    - User model                         │  │
│    - Password hashing                   │  │
│    - Authentication                     │  │
└──────────────────┬──────────────────────┘  │
                   │                          │
                   │                          │
┌──────────────────▼──────────────────────┐  │
│       SQLite Database                   │  │
│       (weather_app.db)                  │  │
│  • users table                          │  │
└─────────────────────────────────────────┘  │
                                              │
                                              │
                                    ┌─────────▼────────────┐
                                    │  Open-Meteo API      │
                                    │  (External Service)  │
                                    │  • Weather data      │
                                    └──────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  config/settings.py                                              │
│  • SECRET_KEY management                                         │
│  • Database URI                                                  │
│  • Weather API URL                                               │
│  • Session configuration                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Features

- 🌡️ **Real-time Weather Data**: Get current weather information using Open-Meteo API (no API key required)
- 👥 **User Management**: Secure user registration and authentication
- 🗄️ **Database Integration**: SQLite database with SQLAlchemy ORM
- 🏗️ **Modular Architecture**: Industrial-grade, modularized code structure
- 🔒 **Security**: Password hashing, session management, and secure authentication
- ✅ **Code Quality**: Ruff linting with all rules enabled
- 🧪 **Comprehensive Tests**: Unit tests with pytest and coverage reporting
- 🚀 **CI/CD Pipeline**: GitHub Actions for automated testing and building
- 📦 **Distribution Ready**: Modern pyproject.toml for packaging and distribution

## Project Structure

```
weather-app/
├── backend/
│   ├── config/          # Configuration settings
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── tests/           # Unit tests
│   ├── database.py      # Database initialization
│   └── app.py           # Main application
├── frontend/
│   ├── static/
│   │   ├── css/        # Stylesheets
│   │   └── js/         # JavaScript files
│   └── templates/      # HTML templates
├── .github/
│   └── workflows/      # CI/CD configurations
├── pyproject.toml      # Project configuration and dependencies
└── ruff.toml          # Linting configuration
```

## Installation

### Prerequisites

- Python 3.12 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/poiuytrezaur/genai_test.git
cd genai_test
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. (Optional) Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### Running the Application

Start the Flask server:
```bash
python backend/app.py
```

Or using the installed console script:
```bash
weather-app
```

The application will be available at `http://localhost:5000`

### Environment Variables

You can configure the application using environment variables:

- `SECRET_KEY`: Secret key for session management (default: "dev-secret-key-change-in-production")
- `DATABASE_URL`: Database connection URL (default: SQLite in project root)
- `PORT`: Server port (default: 5000)
- `FLASK_DEBUG`: Enable debug mode (default: False)

Example:
```bash
export SECRET_KEY="your-secret-key"
export PORT=8000
python backend/app.py
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user information

### Weather

- `GET /api/weather/current?latitude={lat}&longitude={lon}` - Get current weather

### Frontend Routes

- `/` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/weather` - Weather dashboard (requires authentication)

## Testing

Run the test suite:
```bash
pytest backend/tests/ -v
```

Run with coverage:
```bash
pytest backend/tests/ -v --cov=backend --cov-report=html
```

## Code Quality

This project uses Ruff with all rules enabled for code quality.

Run linting:
```bash
ruff check .
```

Run formatting:
```bash
ruff format .
```

Fix auto-fixable issues:
```bash
ruff check --fix .
```

## Building and Distribution

Build the distribution package:
```bash
python -m build
```

This creates both wheel and source distributions in the `dist/` directory.

Install from the distribution:
```bash
pip install dist/weather_app-1.0.0-py3-none-any.whl
```

## CI/CD

The project includes a GitHub Actions workflow that:

1. **Lints** code with Ruff
2. **Runs tests** with pytest and coverage
3. **Builds** distribution packages
4. **Performs security scans** with Bandit and Safety

The workflow runs on pushes and pull requests to `main` and `develop` branches.

## Database

The application uses SQLite by default. The database file `weather_app.db` is created automatically on first run.

To use a different database, set the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost/weatherapp"
```

## Security

- Passwords are hashed using Werkzeug's security utilities
- Sessions are secured with HTTP-only cookies
- All API endpoints require authentication (except registration and login)
- Environment variables for sensitive configuration

## Development

### Adding New Features

1. Create models in `backend/models/`
2. Add business logic in `backend/services/`
3. Define routes in `backend/routes/`
4. Add tests in `backend/tests/`
5. Run linting and tests

### Code Style

Follow PEP 8 and Google-style docstrings. Use type hints where applicable.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Troubleshooting

### Database Locked Error

If you get a database locked error, ensure no other instances of the app are running.

### Port Already in Use

Change the port using the `PORT` environment variable:
```bash
export PORT=8080
python backend/app.py
```

### Module Not Found

Ensure all dependencies are installed:
```bash
pip install -e .
```

## Acknowledgments

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Built with Flask, SQLAlchemy, and modern web technologies