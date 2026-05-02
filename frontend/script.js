const fileInput = document.getElementById("fileInput");
const viewer = document.getElementById("viewer");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const toggleBtn = document.getElementById("themeToggle");
const loader = document.getElementById("loader");
const modeSelect = document.getElementById("mode");

let uploadedFileName = null;

/* =========================
   THEME TOGGLE
========================= */
toggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("light");
  toggleBtn.textContent =
    document.body.classList.contains("light") ? "☀️" : "🌙";
});

/* =========================
   FILE UPLOAD (REAL BACKEND)
========================= */
fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  viewer.innerHTML = "";

  const progressBar = addProgressMessage(file.name);

  let progress = 0;

  // fake smooth progress
  const interval = setInterval(() => {
    progress += 5;
    if (progress <= 90) {
      progressBar.style.width = progress + "%";
    }
  }, 100);

  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    clearInterval(interval);
    progressBar.style.width = "100%";

    uploadedFileName = data.file;

    addMessage(`✅ ${data.file} is ready`, "bot");

    renderPreview(file);

  } catch (err) {
    clearInterval(interval);
    addMessage("❌ Upload failed", "bot");
    console.error(err);
  }
});

/* =========================
   CHAT (REAL AI CALL)
========================= */
sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  if (!uploadedFileName) {
    addMessage("⚠️ Please upload a document first", "bot");
    return;
  }

  addMessage(text, "user");
  userInput.value = "";

  loader.classList.remove("hidden");

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: text,
        file: uploadedFileName,
        mode: modeSelect.value   // 🔥 NEW
      }),
    });

    const data = await res.json();

    loader.classList.add("hidden");

    addMessageWithTyping(data.answer || "No response");

  } catch (err) {
    loader.classList.add("hidden");
    addMessage("❌ Error talking to AI", "bot");
    console.error(err);
  }
}

/* =========================
   PREVIEW
========================= */
function renderPreview(file) {
  const type = file.type;

  if (type.startsWith("image/")) {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.className = "preview-img";
    viewer.appendChild(img);
  }

  else if (type === "application/pdf") {
    const iframe = document.createElement("iframe");
    iframe.src = URL.createObjectURL(file);
    iframe.className = "preview-pdf";
    viewer.appendChild(iframe);
  }

  else if (type.startsWith("text/")) {
    const reader = new FileReader();

    reader.onload = () => {
      const div = document.createElement("div");
      div.className = "text-preview";
      div.textContent = reader.result;
      viewer.appendChild(div);
    };

    reader.readAsText(file);
  }

  else {
    viewer.innerHTML = "<p>Unsupported file type</p>";
  }
}

/* =========================
   UI HELPERS
========================= */
function addMessage(text, sender) {
  const chatBox = document.getElementById("chatBox");

  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerText = text;

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.scrollTop = chatBox.scrollHeight;
}

function addProgressMessage(fileName) {
  const chatBox = document.getElementById("chatBox");

  const msg = document.createElement("div");
  msg.className = "message bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  bubble.innerHTML = `
    Uploading ${fileName}...
    <div class="progress-container">
      <div class="progress-bar">
        <div class="progress-fill"></div>
      </div>
    </div>
  `;

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.scrollTop = chatBox.scrollHeight;

  return bubble.querySelector(".progress-fill");
}

function typeTextI(element, text, speed = 20){
  let i = 0;
  function typing(){
    if (i<text.length){
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(typing, speed);
    }
  }
  typing();
}

function addMessageWithTyping(text) {
  const chatBox = document.getElementById("chatBox");

  const msg = document.createElement("div");
  msg.className = "message bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  let i = 0;
  function typing() {
    if (i < text.length) {
      bubble.innerHTML += text.charAt(i);
      i++;
      chatBox.scrollTop = chatBox.scrollHeight;
      setTimeout(typing, 15);
    }
  }

  typing();
}
