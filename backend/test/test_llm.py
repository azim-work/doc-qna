from app.core.llm import generate_answer


example_chunks = [
    "Acme offers medical, dental, and vision benefits through SunLife.",
    "Employees are eligible for benefits from the 1st of the following month.",
]
q = "When do benefits begin?"
print(generate_answer(example_chunks, q))
