const body = document.body;
const themeBtn = document.getElementById("themeToggle");

themeBtn.addEventListener("click", () => {
  body.classList.toggle("dark");
  themeBtn.textContent = body.classList.contains("dark") ? "☀️" : "🌙";
});

const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const chatBox = document.getElementById("chatBox");

uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("Select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  addMessage("Uploading document...", "bot");

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("Upload failed");

    const data = await res.json();
    addMessage(data.message || "Document processed successfully!", "bot");

  } catch (err) {
    console.error(err);
    addMessage("Failed to upload document", "bot");
  }
});

const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("userInput");

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  // show loading message
  const loadingMsg = addMessage("Analyzing your document...", "bot");

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: text }) // ✅ correct key
    });

    if (!res.ok) throw new Error("API error");

    const data = await res.json();

    loadingMsg.innerText = data.answer || "No response from AI";

  } catch (err) {
    console.error(err);
    loadingMsg.innerText = "Error getting response from server";
  }
}

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
  return msg;
}