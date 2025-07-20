import { useState } from "react";

function DocumentUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [documentId, setDocumentId] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api/v1/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        setError("Failed to upload document");
        return;
      }

      const data = await response.json();
      console.log("data: ", data);
      setDocumentId(data.document_id);
    } catch (error) {
      setError("Failed to upload document");
      console.error(`Failed to upload document: ${error}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      <form onSubmit={onSubmit} className="flex flex-col gap-2">
        <label htmlFor="file" className="text-sm font-medium text-gray-700">
          Upload a new document (PDF).
        </label>
        <input
          id="file"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
        ></input>
        <button
          className="border rounded px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          type="submit"
          disabled={file === null || uploading}
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {error && <p className="text-red-600 mt-4">{error}</p>}
      {documentId && (
        <div className="mt-6 p-4 bg-green-100 text-green-800 rounded">
          <p> Successfully uploaded document. </p>
          <p className="font-semibold">Document ID: {documentId}</p>
        </div>
      )}
    </>
  );
}

export default DocumentUpload;
