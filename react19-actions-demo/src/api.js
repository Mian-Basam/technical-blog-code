// Fake backend calls with artificial latency so pending states are visible.

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const subscribers = new Set();

export async function subscribe(email) {
  await wait(1000);
  if (subscribers.has(email)) {
    throw new Error("This email is already subscribed.");
  }
  subscribers.add(email);
}

export async function sendMessage(text) {
  await wait(1200);
  if (text.toLowerCase().includes("fail")) {
    throw new Error("Message failed to send.");
  }
  return { id: crypto.randomUUID(), text };
}

export async function deleteItem(id) {
  await wait(800);
  return id;
}
