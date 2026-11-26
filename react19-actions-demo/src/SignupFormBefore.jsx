import { useState } from "react";
import { subscribe } from "./api.js";

// The pre-React 19 version: four pieces of state and a handler.
export function SignupFormBefore() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [isPending, setIsPending] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsPending(true);
    setError(null);
    setSuccess(false);
    try {
      await subscribe(email);
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsPending(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        placeholder="you@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button disabled={isPending}>{isPending ? "Subscribing..." : "Subscribe"}</button>
      {error && <p className="error">{error}</p>}
      {success && <p className="success">Thanks for subscribing!</p>}
    </form>
  );
}
