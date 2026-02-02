import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Organisations from "./pages/Organisations";
import UserAccount from "./pages/UserAccount.tsx";
import Vehicules from "./pages/Vehicules.tsx";
import Drivers from "./pages/Drivers.tsx";

export default function App() {
  const [authenticated, setAuthenticated] = useState(
    Boolean(localStorage.getItem("token"))
  );
  const [mode, setMode] = useState<"login" | "register">("login");
const [page, setPage] = useState<"orgs" | "account" | "vehicules" | "drivers">("orgs");

  if (!authenticated) {
    return (
      <div style={{ padding: 20 }}>

        {mode === "login" ? (
          <>
            <Login onAuth={() => setAuthenticated(true)} />
            <p>
              No account?{" "}
              <button onClick={() => setMode("register")}>
                Register
              </button>
            </p>
          </>
        ) : (
          <>
            <Register onAuth={() => setAuthenticated(true)} />
            <p>
              Already have an account?{" "}
              <button onClick={() => setMode("login")}>
                Login
              </button>
            </p>
          </>
        )}
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Fleetcore</h1>
<button onClick={() => setPage("orgs")}>Organisations</button>
<button onClick={() => setPage("vehicules")}>Vehicules</button>
<button onClick={() => setPage("drivers")}>Drivers</button>
 <button onClick={() => setPage("account")}>My account</button>


      <button
        onClick={() => {
          localStorage.removeItem("token");
          setAuthenticated(false);
        }}
      >
        Logout
      </button>
        {page === "orgs" && <Organisations />}
        {page === "account" && <UserAccount />}
        {page === "vehicules" && <Vehicules/>}
        {page === "drivers" && <Drivers/>}
    </div>
  );
}
