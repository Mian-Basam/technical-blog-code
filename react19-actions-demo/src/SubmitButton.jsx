import { useFormStatus } from "react-dom";

// Reads the pending state of the <form> that contains it.
export function SubmitButton({ children, pendingText = "Working..." }) {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? pendingText : children}
    </button>
  );
}
