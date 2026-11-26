import { useOptimistic, useState } from "react";
import { sendMessage } from "./api.js";
import { SubmitButton } from "./SubmitButton.jsx";

export function Messages() {
  const [messages, setMessages] = useState([
    { id: "1", text: "Welcome! Type a message (include 'fail' to see a rollback)." },
  ]);
  const [error, setError] = useState(null);
  const [optimisticMessages, addOptimistic] = useOptimistic(
    messages,
    (current, newText) => [...current, { id: `temp-${newText}`, text: newText, sending: true }]
  );

  async function sendAction(formData) {
    const text = String(formData.get("message") ?? "").trim();
    if (!text) return;
    setError(null);
    addOptimistic(text); // shows immediately
    try {
      const saved = await sendMessage(text);
      setMessages((prev) => [...prev, saved]); // real data replaces it
    } catch (err) {
      setError(err.message); // optimistic item disappears on its own
    }
  }

  return (
    <>
      <ul className="messages">
        {optimisticMessages.map((m) => (
          <li key={m.id} className={m.sending ? "muted" : ""}>
            {m.text} {m.sending && <small>(sending...)</small>}
          </li>
        ))}
      </ul>
      <form action={sendAction}>
        <input name="message" placeholder="Say something" autoComplete="off" />
        <SubmitButton pendingText="Sending...">Send</SubmitButton>
      </form>
      {error && <p className="error">{error}</p>}
    </>
  );
}
