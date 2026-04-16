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
let activeFile = null;

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

  const url = URL.createObjectURL(file);

  // ✅ SHOW PREVIEW IMMEDIATELY (before upload)
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
      <div style="color: #888; text-align:center;">
        <p>${file.name}</p>
        <p>Preview not supported</p>
      </div>
    `;
  }

  // ✅ THEN upload file
  uploadFile(file);
});

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

  const loadingMsg = addMessage("Uploading...", "bot");

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error();

    const data = await res.json();

    // ✅ IMPORTANT: set active file
    activeFile = data.file;

    loadingMsg.innerText = "Document ready! Ask something.";

    console.log("Active file:", activeFile);

  } catch {
    loadingMsg.innerText = "Upload failed";
  }
}
/* CHAT */
sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {
  const text = input.value.trim();

  if (!text || !activeFile) {
    alert("Upload a file first!");
    return;
  }

  addMessage(text, "user");
  input.value = "";

  const loadingMsg = addMessage("...", "bot");

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: text,
        file: activeFile, // 🔥 KEY FIX
      }),
    });

    const data = await res.json();

    loadingMsg.innerText = data.answer;

  } catch {
    loadingMsg.innerText = "Error";
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