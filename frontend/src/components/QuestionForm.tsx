import { useState } from "react";

type Props = {
  onSubmit: (question: string) => void;
  loading: boolean;
};

function QuestionForm({ onSubmit, loading }: Props) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    onSubmit(question);
    setQuestion(""); // Clear the input after submission
  };

  return (
    <>
      <h1 className="text-2xl font-bold mb-4">Ask a Question</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Submit"}
        </button>
      </form>
    </>
  );
}

export default QuestionForm;
