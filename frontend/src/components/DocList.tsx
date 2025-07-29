import type { Document } from "../types";

interface Props {
  documents: Document[];
}

function DocList({ documents }: Props) {
  return (
    <ul className="space-y-2 mt-4">
      {documents.map((document) => (
        <li
          key={document.doc_id}
          className="text-sm text-gray-700 truncate  pb-1"
        >
          📄 {document.filename}
        </li>
      ))}
    </ul>
  );
}

export default DocList;
