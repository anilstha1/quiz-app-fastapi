import pytest
from fastapi.testclient import TestClient
from app.database import Question, Base, engine, SessionLocal
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def test_db():
    # Create the test database and tables
    Base.metadata.create_all(bind=engine)

    # Create a test session
    db = SessionLocal()

    # Add test data
    test_questions = [
        Question(
            question="Test Question 1?",
            options=["A", "B", "C", "D"],
            answer="A"
        ),
        Question(
            question="Test Question 2?",
            options=["1", "2", "3", "4"],
            answer="2"
        )
    ]

    for question in test_questions:
        db.add(question)
    db.commit()

    yield db  # provide the test database to the tests

    # Cleanup - drop all tables
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Quiz App!"}


def test_read_quiz():
    """Test getting all quiz questions without answers"""
    response = client.get("/quiz")
    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "quiz" in data
    assert "message" in data
    assert data["message"] == "Quiz data retrieved successfully!"

    # Check quiz questions
    questions = data["quiz"]
    assert len(questions) >= 2  # We added 2 test questions

    # Verify question format and no answers included
    for question in questions:
        assert "id" in question
        assert "question" in question
        assert "options" in question
        assert "answer" not in question


def test_create_quiz():
    """Test creating a new quiz question"""
    new_question = {
        "question": "What is the capital of Nepal?",
        "options": ["Kathmandu", "Pokhara", "Lalitpur", "Bharatpur"],
        "answer": "Kathmandu"
    }

    response = client.post("/quiz", json=new_question)
    assert response.status_code == 200
    data = response.json()

    # Check response
    assert data["message"] == "Quiz question created successfully!"
    assert "question" in data
    created_question = data["question"]

    # Verify created question data
    assert created_question["question"] == new_question["question"]
    assert created_question["options"] == new_question["options"]
    assert created_question["answer"] == new_question["answer"]


def test_submit_quiz_correct_answers():
    """Test submitting quiz answers with correct answers"""
    answers = [
        {"id": 1, "answer": "A"},
        {"id": 2, "answer": "2"}
    ]

    response = client.post("/quiz/submit", json=answers)
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Quiz submitted successfully!"
    assert data["correct_answers"] == 2
    assert data["total_questions"] >= 2


def test_submit_quiz_wrong_answers():
    """Test submitting quiz answers with wrong answers"""
    answers = [
        {"id": 1, "answer": "B"},
        {"id": 2, "answer": "3"}
    ]

    response = client.post("/quiz/submit", json=answers)
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Quiz submitted successfully!"
    assert data["correct_answers"] == 0
    assert data["total_questions"] >= 2


def test_submit_quiz_invalid_question_id():
    """Test submitting answers with invalid question ID"""
    answers = [
        {"id": 6, "answer": "A"}
    ]

    response = client.post("/quiz/submit", json=answers)
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]
