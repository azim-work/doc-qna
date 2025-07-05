import { useState } from "react";
import QuestionForm from "./QuestionForm";

const documentId = "c18c7ccf-27ad-4caf-b921-c10b2194ac4a";

function QNASection() {
  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");

  const handleAskQuestion = async (question: string) => {
    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const res = await fetch("http://localhost:8000/api/v1/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_id: documentId,
          question: question,
        }),
      });

      if (!res.ok) throw new Error("Request failed");

      const data: { answer: string } = await res.json();
      if (!data.answer) throw new Error("No answer found");
      setAnswer(data.answer);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex-1 p-6 bg-white rounded shadow">
      <QuestionForm onSubmit={handleAskQuestion} loading={loading} />
      {error && <p className="text-red-600 mt-4">{error}</p>}

      {answer && (
        <div className="mt-6 p-4 bg-green-100 text-green-800 rounded">
          <p className="font-semibold">Answer:</p>
          <p>{answer}</p>
        </div>
      )}
    </main>
  );
}

export default QNASection;
