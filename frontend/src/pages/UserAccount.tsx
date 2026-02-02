import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function UserAccount() {
  const [user, setUser] = useState<any>(null);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/users/me")
      .then(setUser)
      .catch((err) => setError(err.message));
  }, []);

  async function save() {
    try {
      await api("/users/me", {
        method: "PUT",
        body: JSON.stringify({
          name: user.name,
          email: user.email,
        }),
      });

      setEditing(false);
      setError("");
    } catch (err: any) {
      setError(err.message);
    }
  }

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h2>My account</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!editing ? (
        <>
          <p>
            <strong>Name:</strong> {user.name}
          </p>
          <p>
            <strong>Email:</strong> {user.email}
          </p>

          <button onClick={() => setEditing(true)}>Edit</button>
        </>
      ) : (
        <>
          <input
            value={user.name}
            onChange={(e) =>
              setUser({ ...user, name: e.target.value })
            }
            placeholder="Name"
          />
          <br />

          <input
            value={user.email}
            onChange={(e) =>
              setUser({ ...user, email: e.target.value })
            }
            placeholder="Email"
          />
          <br />

          <button onClick={save}>Save</button>
          <button onClick={() => setEditing(false)}>Cancel</button>
        </>
      )}
    </div>
  );
}
