const body = document.body;
const themeBtn = document.getElementById("themeToggle");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const chatBox = document.getElementById("chatBox");
const viewer = document.getElementById("viewer");
const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("userInput");

// 🌙 Theme toggle
themeBtn.addEventListener("click", () => {
  body.classList.toggle("dark");
  themeBtn.textContent = body.classList.contains("dark") ? "☀️" : "🌙";
});

// 📂 Open file picker
uploadBtn.addEventListener("click", () => fileInput.click());

// 👀 Preview file + upload
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);

  if (file.type.startsWith("image/")) {
    viewer.innerHTML = `<img src="${url}" class="preview-img" />`;
  } else if (file.type === "application/pdf") {
    viewer.innerHTML = `<iframe src="${url}" class="preview-pdf"></iframe>`;
  } else {
    viewer.innerHTML = `<p>Preview not supported</p>`;
  }

  uploadFile(file);
});

// 🚀 Upload
async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const loadingMsg = addMessage("📤 Uploading document...", "bot");

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    loadingMsg.innerText = data.message || "✅ Document ready!";

  } catch {
    loadingMsg.innerText = "❌ Upload failed";
  }
}

// 💬 Chat
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const loadingMsg = addMessage("...", "bot");

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: text })
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    typeText(loadingMsg, data.answer || "No response");

  } catch {
    loadingMsg.innerText = "❌ Error";
  }
}

// ✨ Typing effect
function typeText(el, text) {
  el.innerText = "";
  let i = 0;

  const interval = setInterval(() => {
    el.innerText += text[i];
    i++;
    if (i >= text.length) clearInterval(interval);
  }, 15);
}

// 💬 Add message
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerText = text;

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.scrollTop = chatBox.scrollHeight;

  return bubble;
}