import DocumentUpload from "./DocumentUpload";

function Sidebar() {
  return (
    <aside className="w-1/3 bg-white p-6 shadow-md">
      <h2 className="text-xl font-semibold mb-4">Documents</h2>
      <DocumentUpload />
    </aside>
  );
}

export default Sidebar;
