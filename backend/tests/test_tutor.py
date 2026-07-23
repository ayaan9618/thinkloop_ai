from backend.app.services.tutor import TutorService


def test_ask_question(db_session):
    """Test asking a question."""
    service = TutorService(db_session)
    result = service.ask_question("user123", "What is binary search?")
    
    assert "conversation_id" in result
    assert "response" in result
    assert result["hint_level"] == 0
    assert result["can_request_hint"] is True


def test_ask_what_question(db_session):
    """Test 'what' question gets specific response."""
    service = TutorService(db_session)
    result = service.ask_question("user123", "What is recursion?")
    
    assert "What do you already know" in result["response"]


def test_ask_how_question(db_session):
    """Test 'how' question gets specific response."""
    service = TutorService(db_session)
    result = service.ask_question("user123", "How do I solve this?")
    
    assert "similar problems" in result["response"]


def test_request_hint(db_session):
    """Test requesting a hint."""
    service = TutorService(db_session)
    result = service.get_hint("user123", "conv123", hint_level=0)
    
    assert "hint" in result
    assert result["hint_level"] == 1


def test_reveal_answer(db_session):
    """Test revealing answer."""
    service = TutorService(db_session)
    result = service.reveal_answer("user123", "conv123")
    
    assert "answer" in result
    assert "explanation" in result
