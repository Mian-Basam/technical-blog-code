# React 19 Actions Demo

Companion code for the article **[React 19: Understanding Actions and useActionState](https://mian-basam.github.io/blog/react-19-actions-and-useactionstate/)**.

A small Vite app with four live examples:

1. **Before:** a signup form with `useState` and `onSubmit`
2. **After:** the same form with `useActionState` and a reusable `useFormStatus` submit button
3. **`useOptimistic`:** a message list that shows messages instantly and rolls back on failure (include the word "fail" in a message)
4. **`useTransition`:** async Actions outside of forms

The backend is faked in `src/api.js` with artificial delays, so you can see pending states.

## Run it

Requires Node.js 18+.

```bash
npm install
npm run dev
```

Then open the URL Vite prints (usually http://localhost:5173).

## Files

```text
src/
├── api.js               Fake async backend
├── SignupFormBefore.jsx Pre-React 19 form
├── SignupForm.jsx       useActionState version
├── SubmitButton.jsx     useFormStatus button
├── Messages.jsx         useOptimistic example
├── DeleteButton.jsx     useTransition example
└── App.jsx              Puts it all together
```
