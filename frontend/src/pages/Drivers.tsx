import { useEffect, useState } from "react";
import { api } from "../api/client";

type Driver = {
  id: string;
  name: string;
  organisation_id: string;
};

type Organisation = {
  id: string;
  name: string;
};

type Vehicule = {
  id: string;
  plate_number: string;
  name: string;
  organisation_id: string;
};


export default function Drivers() {
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [organisations, setOrganisations] = useState<Organisation[]>([]);
  const [filterOrg, setFilterOrg] = useState("");
  const [editingDriver, setEditingDriver] = useState<any | null>(null);
  const [error, setError] = useState("");
const [selectedDriver, setSelectedDriver] = useState<Driver | null>(null);
const [vehicules, setVehicules] = useState<Vehicule[]>([]);
const [selectedVehicule, setSelectedVehicule] = useState("");
const [currentAssignment, setCurrentAssignment] = useState<any | null>(null);

  useEffect(() => {
    api<Organisation[]>("/organisations/")
      .then(setOrganisations)
      .catch((err) => setError(err.message));
  }, []);


  useEffect(() => {
    const query = filterOrg ? `?organisation_id=${filterOrg}` : "";
    api<Driver[]>(`/drivers/${query}`)
      .then(setDrivers)
      .catch((err) => setError(err.message));
  }, [filterOrg]);

useEffect(() => {
  if (!selectedDriver) return;

  api(`/assignments/active?driver_id=${selectedDriver.id}`)
    .then(setCurrentAssignment)
    .catch(() => setCurrentAssignment(null));
}, [selectedDriver]);


useEffect(() => {
  if (!selectedDriver) return;

  api(`/vehicules/?organisation_id=${selectedDriver.organisation_id}`)
    .then(setVehicules)
    .catch((err) => setError(err.message));
}, [selectedDriver]);

  async function saveDriver() {
    try {
      const method = editingDriver.id ? "PUT" : "POST";
      const url = editingDriver.id
        ? `/drivers/${editingDriver.id}`
        : "/drivers/";

    if (!editingDriver.organisation_id) {
          setError("Please select an organisation");
          return;
        }
    if (!editingDriver.name) {
          setError("Driver name is required");
          return;
        }
      await api(url, {
        method,
        body: JSON.stringify({
          name: editingDriver.name,
          organisation_id: editingDriver.organisation_id,
        }),
      });

      setEditingDriver(null);
      setError("");

      const query = filterOrg ? `?organisation_id=${filterOrg}` : "";
      setDrivers(await api(`/drivers/${query}`));
    } catch (err: any) {
      setError(err.message);
    }
  }
  async function assignVehicule() {
  if (!selectedDriver || !selectedVehicule) {
    setError("Please select a vehicle");
    return;
  }

  try {
    await api("/assignments", {
      method: "POST",
      body: JSON.stringify({
        vehicule_id: selectedVehicule,
        driver_id: selectedDriver.id
      }),
    });

    setError("");
    alert("Vehicle assigned successfully");

    setCurrentAssignment(
      await api(`/assignments/active?driver_id=${selectedDriver.id}`)
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

  async function deleteDriver(id: string) {
    if (!window.confirm("Delete this driver?")) return;

    try {
      await api(`/drivers/${id}`, { method: "DELETE" });

      const query = filterOrg ? `?organisation_id=${filterOrg}` : "";
      setDrivers(await api(`/drivers/${query}`));
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Drivers</h2>

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
          setEditingDriver({ name: "", organisation_id: "" })
        }
      >
        Add driver
      </button>

      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Organisation</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {drivers.map((d) => (
            <tr key={d.id}>
              <td>{d.name}</td>
              <td>
                {organisations.find((o) => o.id === d.organisation_id)?.name ||
                  "-"}
              </td>
              <td>
                <button onClick={() => setEditingDriver(d)}>Edit</button>
                <button onClick={() => deleteDriver(d.id)}>Delete</button>
                <button onClick={() => setSelectedDriver(d)}>Assign vehicle</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {editingDriver && (
        <div style={{ marginTop: 20 }}>
          <h3>{editingDriver.id ? "Edit driver" : "Add driver"}</h3>

          <input
            placeholder="Driver name"
            value={editingDriver.name}
            onChange={(e) =>
              setEditingDriver({
                ...editingDriver,
                name: e.target.value,
              })
            }
          />

          <select
            value={editingDriver.organisation_id}
            onChange={(e) =>
              setEditingDriver({
                ...editingDriver,
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

          <button onClick={saveDriver}>Save</button>
          <button onClick={() => setEditingDriver(null)}>Cancel</button>
        </div>
      )}
        {selectedDriver && (
  <div style={{ marginTop: 30, borderTop: "1px solid #ccc", paddingTop: 20 }}>
    <h3>
      Vehicle assignment for driver:{" "}
      <strong>{selectedDriver.name}</strong>
    </h3>

    {currentAssignment ? (
      <>
        <p>
          <strong>Current vehicle:</strong>{" "}
          {
            vehicules.find(
              (v) => v.id === currentAssignment.vehicule_id
            )?.plate_number
          }
        </p>

        <button onClick={endAssignment}>End assignment</button>
      </>
    ) : (
      <>
        <select
          value={selectedVehicule}
          onChange={(e) => setSelectedVehicule(e.target.value)}
        >
          <option value="">Select vehicle</option>
          {vehicules.map((v) => (
            <option key={v.id} value={v.id}>
              {v.plate_number}
            </option>
          ))}
        </select>

        <br />

        <button onClick={assignVehicule}>Assign vehicle</button>
      </>
    )}

    <br />

    <button onClick={() => setSelectedDriver(null)}>Close</button>
  </div>
)}

    </div>
  );
}
