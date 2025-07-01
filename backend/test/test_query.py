import requests

DOCUMENT_FILEPATH = "test/acme.pdf"
API_URL = "http://localhost:8000/api/v1"

# Upload document - it will already be indexed
upload_url = f"{API_URL}/upload"
with open(DOCUMENT_FILEPATH, "rb") as f:
    files = {"file": f}
    response = requests.post(upload_url, files=files)

if response.status_code != 200:
    print("Error uploading document:", response.text)
    exit(1)

data = response.json()
document_id = data["document_id"]
print("Document ID:", document_id)
print("-" * 60)

# List of test questions and optional expected answers
questions = [
    ("When do benefits begin?", "From the 1st of the following month"),
    ("What is the policy for vacation time?", "15 paid vacation days per year"),
    ("Is dental insurance included?", "Yes, through SunLife"),
    ("Are employees eligible for benefits immediately?", "No, from the next month"),
    ("Do benefits start from day one or the next month?", "Next month"),
    ("Does Acme offer stock options?", "I don't know"),
    ("How does the cafeteria subsidy work?", "I don't know"),
    ("How do I get reimbursed for a doctor’s visit?", "Submit a claim through SunLife"),
    (
        "Tell me about when coverage starts after joining",
        "From the 1st of the next month",
    ),
    ("How are employee benefits managed?", "Through SunLife, supported by HR"),
    ("Who is responsible for employee health insurance?", "SunLife, coordinated by HR"),
]

# Query each question
query_url = f"{API_URL}/query"
for question, expected_answer in questions:
    payload = {
        "document_id": document_id,
        "question": question,
    }
    response = requests.post(query_url, json=payload)

    if response.status_code != 200:
        print(f"❌ Error for question: {question}")
        print("Error:", response.text)
        print("-" * 60)
        continue

    data = response.json()
    actual_answer = data["answer"]

    print(f"🧠 Question: {question}")
    print(f"🔍 Expected: {expected_answer}")
    print(f"💬 Answered: {actual_answer}")
    print("-" * 60)
