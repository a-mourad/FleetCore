
import { useState } from "react";
import { login, register } from "../api/auth";

export default function Register({ onAuth }: { onAuth: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin() {
    try {

          if ( !email || !password) {
            setError("All fields are required");
            return;
          }
      const res = await login(email, password);
      localStorage.setItem("token", res.access_token);
      onAuth();
    } catch (err: any) {
    setError(err.message || "Login failed");
  }
  }



  return (
    <div>
      <h2>Login / Register</h2>

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

      <button onClick={handleLogin}>Login</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
