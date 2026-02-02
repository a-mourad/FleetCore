import { useEffect, useState } from "react";
import { api } from "../api/client";


type Organisation = {
  id: string;
  name: string;
  parent_id?: string | null;
};

export default function Organisations() {


  const [orgs, setOrgs] = useState<Organisation[]>([]);
  const [name, setName] = useState("");
  const [selectedParent, setSelectedParent] = useState<Record<string, string>>({});
  const [editedNames, setEditedNames] = useState<Record<string, string>>({});
    const [editingOrg, setEditingOrg] = useState<any | null>(null);
    const [error, setError] = useState("");


    const orgMap = Object.fromEntries(
      orgs.map((o) => [o.id, o.name])
    );

  useEffect(() => {
    api<Organisation[]>("/organisations").then(setOrgs);
  }, []);

async function updateOrganisation() {
  try {
    await api(`/organisations/${editingOrg.id}`, {
      method: "PUT",
      body: JSON.stringify({
        name: editingOrg.name,
        parent_id: editingOrg.parent_id,
      }),
    });

    setEditingOrg(null);
    setOrgs(await api("/organisations/"));
  } catch (err: any) {
    setError(err.message || "Update failed");
  }
}
async function deleteOrganisation(orgId: string) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this organisation?"
  );

  if (!confirmed) return;

  try {
    await api(`/organisations/${orgId}`, {
      method: "DELETE",
    });

    setError("");
    setOrgs(await api("/organisations/"));
  } catch (err: any) {
    setError(err.message || "Failed to delete organisation");
  }
}


  async function createOrg() {
    if (!name.trim()){
        setError("Name is required");
        return;
    }
    try {
            await api("/organisations", {
      method: "POST",
      body: JSON.stringify({ name }),
    });

    setName("");
    setOrgs(await api("/organisations"));
    } catch (err: any) {
    setError(err.message || "Update failed");
  }

  }

  return (
    <div>
      <h2>Organisations</h2>
{error && <p style={{ color: "red" }}>{error}</p>}

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Organisation name"
      />
      <button onClick={createOrg}>Create</button>

      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Parent</th>
          </tr>
        </thead>
      <tbody>
  {orgs.map((o) => (
    <tr key={o.id}>
      <td>{o.name}</td>
      <td>{o.parent_id ? orgMap[o.parent_id] : "-"}</td>
      <td>
        <button onClick={() => setEditingOrg(o)}>Edit</button>
        <button onClick={() => deleteOrganisation(o.id)}>Delete</button>
      </td>
    </tr>
  ))}
</tbody>


      </table>
        {editingOrg && (
  <div style={{ marginTop: 20, border: "1px solid #ccc", padding: 10 }}>
    <h3>Edit organisation</h3>

    <input
      value={editingOrg.name}
      onChange={(e) =>
        setEditingOrg({ ...editingOrg, name: e.target.value })
      }
      placeholder="Organisation name"
    />

    <select
      value={editingOrg.parent_id || ""}
      onChange={(e) =>
        setEditingOrg({
          ...editingOrg,
          parent_id: e.target.value || null,
        })
      }
    >
      <option value="">No parent</option>
      {orgs
        .filter((o) => o.id !== editingOrg.id)
        .map((o) => (
          <option key={o.id} value={o.id}>
            {o.name}
          </option>
        ))}
    </select>

    <br />

    <button onClick={updateOrganisation}>Save</button>
    <button onClick={() => setEditingOrg(null)}>Cancel</button>
  </div>
)}

    </div>
  );
}
