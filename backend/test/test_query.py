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
print("document_id: ", document_id)

# Query document
query_url = f"{API_URL}/query"
payload = {
    "document_id": document_id,
    "question": "Where can I submit health claims?",
}
response = requests.post(query_url, json=payload)

if response.status_code != 200:
    print("Error querying document:", response.text)
    exit(1)

data = response.json()
answer = data["answer"]
print("answer: ", answer)
