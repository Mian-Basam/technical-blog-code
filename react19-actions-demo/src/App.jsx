import { SignupFormBefore } from "./SignupFormBefore.jsx";
import { SignupForm } from "./SignupForm.jsx";
import { Messages } from "./Messages.jsx";
import { DeleteDemo } from "./DeleteButton.jsx";

export default function App() {
  return (
    <main>
      <h1>React 19 Actions Demo</h1>
      <p className="muted">
        Companion code for “React 19: Understanding Actions and useActionState”.
        Subscribing the same email twice shows the error path.
      </p>

      <section>
        <h2>1. Before: useState + onSubmit</h2>
        <SignupFormBefore />
      </section>

      <section>
        <h2>2. After: useActionState + useFormStatus</h2>
        <SignupForm />
      </section>

      <section>
        <h2>3. useOptimistic</h2>
        <Messages />
      </section>

      <section>
        <h2>4. Actions outside forms: useTransition</h2>
        <DeleteDemo />
      </section>
    </main>
  );
}
