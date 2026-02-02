import { useEffect, useState } from "react";
import { api } from "../api/client";

type Vehicule = {
  id: string;
  plate_number: string;
  name: string;
  organisation_id: string;
};

type Organisation = {
  id: string;
  name: string;
};
type Driver = {
  id: string;
  name: string;
};

export default function Vehicules() {
  const [vehicules, setVehicules] = useState<Vehicule[]>([]);
  const [organisations, setOrganisations] = useState<Organisation[]>([]);
  const [filterOrg, setFilterOrg] = useState("");
  const [editingVehicule, setEditingVehicule] = useState<any | null>(null);
  const [error, setError] = useState("");
const [selectedVehicle, setSelectedVehicle] = useState<Vehicule | null>(null);
const [drivers, setDrivers] = useState<Driver[]>([]);
const [selectedDriver, setSelectedDriver] = useState("");
const [currentAssignment, setCurrentAssignment] = useState<{
  id: string;
  driver_id: string;
} | null>(null);



  useEffect(() => {
    api<Organisation[]>("/organisations/")
      .then(setOrganisations)
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    const query = filterOrg ? `?organisation_id=${filterOrg}` : "";
    api<Vehicule[]>(`/vehicules/${query}`)
      .then(setVehicules)
      .catch((err) => setError(err.message));
  }, [filterOrg]);
useEffect(() => {
  if (!selectedVehicle) return;

  api(`/drivers/?organisation_id=${selectedVehicle.organisation_id}`)
    .then(setDrivers)
    .catch((err) => setError(err.message));
}, [selectedVehicle]);
useEffect(() => {
  if (!selectedVehicle) return;

  api(`/assignments/active?vehicule_id=${selectedVehicle.id}`)
    .then(setCurrentAssignment)
    .catch(() => setCurrentAssignment(null));
}, [selectedVehicle]);

  async function saveVehicule() {
    try {
      const method = editingVehicule.id ? "PUT" : "POST";
      const url = editingVehicule.id
        ? `/vehicules/${editingVehicule.id}`
        : "/vehicules/";

    if (!editingVehicule.organisation_id) {
          setError("Please select an organisation");
          return;
        }
    if (!editingVehicule.plate_number) {
          setError("Plate number is required");
          return;
        }
      await api(url, {
        method,
        body: JSON.stringify({
          plate_number: editingVehicule.plate_number,
          name: editingVehicule.name,
          organisation_id: editingVehicule.organisation_id,
        }),
      });

      setEditingVehicule(null);
      setError("");

      const query = filterOrg ? `?organisation_id=${filterOrg}` : "";
      setVehicules(await api(`/vehicules/${query}`));
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function deleteVehicule(id: string) {
    if (!window.confirm("Delete this vehicule?")) return;

    try {
      await api(`/vehicules/${id}`, { method: "DELETE" });

      const query = filterOrg ? `?organisation_id=${filterOrg}` : "";
      setVehicules(await api(`/vehicules/${query}`));
    } catch (err: any) {
      setError(err.message);
    }
  }

async function assignDriver() {
  if (!selectedVehicle) return;

  if (!selectedDriver) {
    setError("Please select a driver");
    return;
  }

  try {
    await api("/assignments", {
      method: "POST",
      body: JSON.stringify({
        vehicule_id: selectedVehicle.id,
        driver_id: selectedDriver
      }),
    });

    setError("");
    setSelectedDriver("");
    alert("Driver assigned successfully");

    setCurrentAssignment(
      await api(`/assignments/active?vehicule_id=${selectedVehicle.id}`)
    );
  } catch (err: any) {
    setError(err.message);
  }
}
async function endAssignment() {
  if (!currentAssignment) return;

  try {
    await api(`/assignments/${currentAssignment.id}/end`, {
      method: "POST"
    });

    setError("");
    setCurrentAssignment(null);
    alert("Assignment ended");
  } catch (err: any) {
    setError(err.message);
  }
}

  return (
    <div>
      <h2>Vehicules</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <select
        value={filterOrg}
        onChange={(e) => setFilterOrg(e.target.value)}
      >
        <option value="">All organisations</option>
        {organisations.map((o) => (
          <option key={o.id} value={o.id}>
            {o.name}
          </option>
        ))}
      </select>

      <button
        onClick={() =>
          setEditingVehicule({ plate_number: "", organisation_id: "",name:"" })
        }
      >
        Add vehicule
      </button>

      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Plate</th>
            <th>Name</th>
            <th>Organisation</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {vehicules.map((v) => (
            <tr key={v.id}>
              <td>{v.plate_number}</td>
              <td>{v.name}</td>
              <td>
                {organisations.find((o) => o.id === v.organisation_id)?.name ||
                  "-"}
              </td>
              <td>
                <button onClick={() => setEditingVehicule(v)}>Edit</button>
                <button onClick={() => deleteVehicule(v.id)}>Delete</button>
                  <button onClick={() => setSelectedVehicle(v)}>  Assign driver </button>

              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {editingVehicule && (
        <div style={{ marginTop: 20 }}>
          <h3>{editingVehicule.id ? "Edit vehicule" : "Add vehicule"}</h3>

          <input
            placeholder="Plate number"
            value={editingVehicule.plate_number}
            onChange={(e) =>
              setEditingVehicule({
                ...editingVehicule,
                plate_number: e.target.value,
              })
            }
          />
      <input
            placeholder="Name"
            value={editingVehicule.name}
            onChange={(e) =>
              setEditingVehicule({
                ...editingVehicule,
                name: e.target.value,
              })
            }
          />
          <select
            value={editingVehicule.organisation_id}
            onChange={(e) =>
              setEditingVehicule({
                ...editingVehicule,
                organisation_id: e.target.value,
              })
            }
          >
            <option value="">Select organisation</option>
            {organisations.map((o) => (
              <option key={o.id} value={o.id}>
                {o.name}
              </option>
            ))}
          </select>

          <br />

          <button onClick={saveVehicule}>Save</button>
          <button onClick={() => setEditingVehicule(null)}>Cancel</button>
        </div>
      )}
{selectedVehicle && (
  <div style={{ marginTop: 30, borderTop: "1px solid #ccc", paddingTop: 20 }}>
    <h3>
      Assign Driver to vehicle:{" "}
      <strong>{selectedVehicle.plate_number}</strong>
    </h3>


    {currentAssignment ? (
      <>
        <p>
          <strong>Current driver:</strong>{" "}
          {drivers.find(d => d.id === currentAssignment.driver_id)?.name}
        </p>

        <button onClick={endAssignment}>
          End assignment
        </button>
      </>
    ) : (
      <>
        <select
          value={selectedDriver}
          onChange={(e) => setSelectedDriver(e.target.value)}
        >
          <option value="">Select driver</option>
          {drivers.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>

        <br />

        <button onClick={assignDriver}>
          Assign driver
        </button>
      </>
    )}

    <br />

    <button onClick={() => setSelectedVehicle(null)}>
      Close
    </button>
  </div>
)}

    </div>
  );
}
