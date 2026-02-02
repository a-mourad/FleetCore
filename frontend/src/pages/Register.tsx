import { useState } from "react";
import { register } from "../api/auth";

export default function Register({ onAuth }: { onAuth: () => void }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

async function handleRegister() {
  try {
    if (!name || !email || !password) {
      setError("All fields are required");
      return;
    }

    const res = await register(name, email, password);
    localStorage.setItem("token", res.access_token);
    onAuth();
  } catch (err: any) {
    setError(err.message || "Registration failed");
  }
}

  return (
    <div>
      <h2>Register</h2>

      <input
        placeholder="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <br />

      <input
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />

      <input
        type="password"
        placeholder="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />

      <button onClick={handleRegister}>Register</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}