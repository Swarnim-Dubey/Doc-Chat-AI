const body = document.body;
const themeBtn = document.getElementById("themeToggle");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const chatBox = document.getElementById("chatBox");
const viewer = document.getElementById("viewer");
const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("userInput");

themeBtn.addEventListener("click", () => {
  body.classList.toggle("dark");
  themeBtn.textContent = body.classList.contains("dark") ? "☀️" : "🌙";
});

uploadBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);

  if (file.type.startsWith("image/")) {
    viewer.innerHTML = `<img src="${url}" class="preview-img" />`;
  }

  else if (file.type.includes("pdf")) {
    viewer.innerHTML = `<iframe src="${url}" class="preview-pdf"></iframe>`;
  }

  else if (file.type.includes("text") || file.name.endsWith(".txt")) {
    const reader = new FileReader();
    reader.onload = function (e) {
      viewer.innerHTML = `<pre class="text-preview">${e.target.result}</pre>`;
    };
    reader.readAsText(file);
  }

  else {
    viewer.innerHTML = `
      <div class="file-info">
        <p>${file.name}</p>
        <p>Preview not available</p>
      </div>
    `;
  }

  uploadFile(file);
});

async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const loadingMsg = addMessage("Uploading document...", "bot");

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    loadingMsg.innerHTML = formatText(
      data.message || "Document ready! Ask something."
    );
  } catch {
    loadingMsg.innerText = "Upload failed";
  }
}

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
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: text }),
    });

    if (!res.ok) throw new Error();

    const data = await res.json();

    typeText(loadingMsg, data.answer || "No response");
  } catch {
    loadingMsg.innerText = "Error getting response";
  }
}

function typeText(el, text) {
  el.innerHTML = "";
  let i = 0;

  const interval = setInterval(() => {
    el.innerHTML = formatText(text.substring(0, i));
    i++;
    if (i > text.length) clearInterval(interval);
  }, 10);
}

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerHTML = formatText(text);

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.scrollTop = chatBox.scrollHeight;

  return bubble;
}

function formatText(text) {
  return text
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
    .replace(/(\d+\.\s)/g, "<br><br>$1");
}