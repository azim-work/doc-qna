import { useState } from "react";

function Sidebar() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [documentId, setDocumentId] = useState("");

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError("");
    setDocumentId("");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const res = await fetch("http://localhost:8000/api/v1/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setDocumentId(data.document_id);
    } catch (err) {
      console.error("Upload error:", err);
      setError("Something went wrong. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <aside className="w-1/3 bg-white p-4 shadow-md">
      <h1 className="text-2xl font-bold mb-4">Documents</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
        className="mb-2"
      />

      <button
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {documentId && (
        <div className="mt-6 p-4  text-sm bg-green-100 text-green-800">
          <span className="font-semibold">Document ID:</span> {documentId}
        </div>
      )}
    </aside>
  );
}

export default Sidebar;
