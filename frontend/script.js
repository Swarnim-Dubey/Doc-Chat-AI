// testing

const chatBox = document.getElementById("chatBox");

function addMessage(content, role) {
  const div = document.createElement("div");
  div.classList.add("message", role);
  div.textContent = content;
  chatBox.appendChild(div);

  chatBox.scrollTop = chatBox.scrollHeight;
}

// 📂 Upload File
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Select a file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    alert("File uploaded successfully!");
  } catch (error) {
    console.error(error);
    alert("Upload failed!");
  }
}

// 💬 Send Message
async function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value;

  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: text }),
    });

    const data = await response.json();

    addMessage(data.answer, "bot");
  } catch (error) {
    console.error(error);
    addMessage("Error connecting to server", "bot");
  }
}