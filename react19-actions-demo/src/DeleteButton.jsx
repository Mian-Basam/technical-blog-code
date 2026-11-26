import { useState, useTransition } from "react";
import { deleteItem } from "./api.js";

// Actions outside forms: useTransition accepts async functions in React 19.
export function DeleteDemo() {
  const [items, setItems] = useState(["Draft post", "Old notes", "Unused image"]);
  const [isPending, startTransition] = useTransition();

  function handleDelete(item) {
    startTransition(async () => {
      await deleteItem(item);
      startTransition(() => {
        setItems((prev) => prev.filter((i) => i !== item));
      });
    });
  }

  return (
    <ul className="items">
      {items.map((item) => (
        <li key={item}>
          {item}{" "}
          <button disabled={isPending} onClick={() => handleDelete(item)}>
            Delete
          </button>
        </li>
      ))}
      {isPending && <li className="muted">Deleting…</li>}
      {items.length === 0 && <li className="muted">Nothing left.</li>}
    </ul>
  );
}
