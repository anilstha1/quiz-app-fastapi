# Quiz App API

This is a simple quiz application built with FastAPI. The application allows you to create quiz questions, get questions without answers, and submit answers to get scores.

## Features

- Create new quiz questions
- Get quiz questions (without answers)
- Submit answers and get scores
- SQLite database for data persistence
- Environment variable support for database configuration

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pydantic for data validation
- python-dotenv for environment variables
- pytest for testing

## Project Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd quiz-app-fastapi
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:

   ```bash
   DATABASE_URL=sqlite:///./quiz.db
   ```

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
