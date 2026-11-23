"""Function calling the Groq LLM API (example from the course page)."""


def ask_groq(question: str, client=None) -> str:
    """Send a question to Groq and return the answer.

    `client` is injectable: production code passes nothing (a real Groq client is
    created), tests pass a mock. This is dependency injection, and it makes mocking easy.
    """
    if not question.strip():
        raise ValueError("Question cannot be empty")
    if client is None:
        from groq import Groq          # imported lazily: tests don't need the package
        client = Groq()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": question}],
        max_tokens=1024,
    )
    return response.choices[0].message.content
