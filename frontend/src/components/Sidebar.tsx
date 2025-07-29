import DocumentUpload from "./DocumentUpload";
import DocList from "./DocList";
import { useState, useEffect } from "react";

function Sidebar() {
  const [documents, setDocuments] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(false);
  const [errorLoadingDocs, setErrorLoadingDocs] = useState("");

  useEffect(() => {
    (async () => {
      setLoadingDocs(true);
      try {
        const response = await fetch(
          "http://localhost:8000/api/v1/list_documents"
        );
        if (!response.ok) {
          setErrorLoadingDocs("Failed to load documents.");
          return;
        }

        // data is an array of documents, like [ {"doc_id": 1, ...} ]
        const data = await response.json();
        setDocuments(data);
      } catch (err) {
        setErrorLoadingDocs("Failed to load documents.");
      } finally {
        setLoadingDocs(false);
      }
    })();
  }, []);

  return (
    <aside className="w-1/3 bg-white p-6 shadow-md flex flex-col gap-4">
      <h2 className="text-xl font-semibold mb-4">Documents</h2>
      <DocumentUpload />
      <hr className="h-px border-t-0 bg-transparent bg-gradient-to-r from-transparent via-neutral-500 to-transparent opacity-25 dark:via-neutral-400" />
      <DocList documents={documents} />
    </aside>
  );
}

export default Sidebar;
