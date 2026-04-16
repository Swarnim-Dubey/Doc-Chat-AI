const body = document.body;
const themeBtn = document.getElementById("themeToggle");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const chatBox = document.getElementById("chatBox");
const viewer = document.getElementById("viewer");
const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("userInput");
const fileList = document.getElementById("fileList");

let files = [];

/* THEME */
themeBtn.addEventListener("click", () => {
  body.classList.toggle("dark");
});

/* RESIZER */
const resizer = document.getElementById("resizer");
const content = document.querySelector(".content");

let isResizing = false;

resizer.addEventListener("mousedown", () => {
  isResizing = true;
});

document.addEventListener("mousemove", (e) => {
  if (!isResizing) return;

  const leftWidth = (e.clientX / window.innerWidth) * 100;
  content.style.gridTemplateColumns = `${leftWidth}% 5px ${100 - leftWidth}%`;
});

document.addEventListener("mouseup", () => {
  isResizing = false;
});

/* FILE HANDLING */
uploadBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  files.push(file);
  renderFileList();
  previewFile(file);
  uploadFile(file);
});

function renderFileList() {
  fileList.innerHTML = "";

  files.forEach((file) => {
    const div = document.createElement("div");
    div.className = "file-item";
    div.innerText = file.name;

    div.onclick = () => previewFile(file);

    fileList.appendChild(div);
  });
}

function previewFile(file) {
  const url = URL.createObjectURL(file);

  if (file.type.startsWith("image/")) {
    viewer.innerHTML = `<img src="${url}" class="preview-img" />`;
  } 
  else if (file.type.includes("pdf")) {
    viewer.innerHTML = `<iframe src="${url}" class="preview-pdf"></iframe>`;
  } 
  else {
    viewer.innerHTML = `<p>Preview not available</p>`;
  }
}

/* API */
async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  addMessage("Uploading...", "bot");

  try {
    await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
  } catch {
    addMessage("Upload failed", "bot");
  }
}

/* CHAT */
sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const bubble = addMessage("", "bot");

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: text }),
    });

    const data = await res.json();
    bubble.innerText = data.answer;

  } catch {
    bubble.innerText = "Error";
  }
}

/* UI */
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerText = text;

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.scrollTop = chatBox.scrollHeight;

  return bubble;
}