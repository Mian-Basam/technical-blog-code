import { useActionState } from "react";
import { subscribe } from "./api.js";
import { SubmitButton } from "./SubmitButton.jsx";

// The action receives the previous state and the form data,
// and returns the next state.
async function subscribeAction(previousState, formData) {
  const email = String(formData.get("email") ?? "");
  if (!email.includes("@")) {
    return { error: "Please enter a valid email.", success: false };
  }
  try {
    await subscribe(email);
    return { error: null, success: true };
  } catch (err) {
    return { error: err.message, success: false };
  }
}

export function SignupForm() {
  const [state, formAction, isPending] = useActionState(subscribeAction, {
    error: null,
    success: false,
  });

  return (
    <form action={formAction}>
      <input name="email" type="email" placeholder="you@example.com" />
      <SubmitButton pendingText="Subscribing...">Subscribe</SubmitButton>
      {isPending && <small className="muted"> talking to the server…</small>}
      {state.error && <p className="error">{state.error}</p>}
      {state.success && <p className="success">Thanks for subscribing!</p>}
    </form>
  );
}
