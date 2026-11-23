"""Mocking: replace the real Groq client with a fake one.

Rule: mock what you don't own (the API), test what you own (our function's logic).
"""
import os
import pytest
from groq_chat import ask_groq


@pytest.fixture
def mock_client(mocker):
    """A fake client whose response has the same shape as the real one."""
    mock_choice = mocker.Mock()
    mock_choice.message.content = "4"
    mock_response = mocker.Mock()
    mock_response.choices = [mock_choice]
    client = mocker.Mock()
    client.chat.completions.create.return_value = mock_response
    return client


def test_ask_groq_returns_answer(mock_client):
    # Arrange: the fixture built the fake client
    # Act
    answer = ask_groq("What is 2+2?", client=mock_client)
    # Assert
    assert answer == "4"


def test_ask_groq_calls_api_correctly(mock_client):
    ask_groq("What is 2+2?", client=mock_client)
    mock_client.chat.completions.create.assert_called_once_with(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        max_tokens=1024,
    )


def test_ask_groq_raises_error_when_api_fails(mocker):
    client = mocker.Mock()
    client.chat.completions.create.side_effect = Exception("API down")
    with pytest.raises(Exception, match="API down"):
        ask_groq("What is 2+2?", client=client)


@pytest.mark.parametrize("question", ["", "   "])
def test_empty_question_never_calls_the_api(mock_client, question):
    with pytest.raises(ValueError, match="cannot be empty"):
        ask_groq(question, client=mock_client)
    mock_client.chat.completions.create.assert_not_called()


@pytest.mark.slow
@pytest.mark.skipif(not os.getenv("GROQ_API_KEY"), reason="needs GROQ_API_KEY and internet (costs tokens)")
def test_real_api_smoke():
    assert ask_groq("Reply with the single digit 4.")
