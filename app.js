import { askAI } from "./ai.js";

const chat = document.getElementById("chat");

function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = `message ${type}`;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    
    // Сохраняем историю
    localStorage.setItem("chatHistory", chat.innerHTML);
}

window.onload = () => {
    const history = localStorage.getItem("chatHistory");
    if (history) {
        chat.innerHTML = history;
    } else {
        addMessage("Здравствуйте! Я помощник Codify.", "bot");
    }
};

async function sendMessage() {
    const input = document.getElementById("message");
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";
    addMessage("Печатает...", "bot");

    try {
        const answer = await askAI(text);
        chat.lastChild.remove();
        addMessage(answer, "bot");
    } catch (error) {
        chat.lastChild.remove();
        addMessage("Ошибка подключения. Попробуйте позже.", "bot");
        console.error("Error:", error);
    }
}

// Глобальные функции для использования в HTML
window.sendMessage = sendMessage;

window.quickAsk = function(text) {
    document.getElementById("message").value = text;
    // Небольшая задержка для корректной отправки
    setTimeout(() => sendMessage(), 50);
};