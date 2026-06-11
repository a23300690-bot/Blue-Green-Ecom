/* chat.js — real-time chat widget */
let chatSocket   = null;
let chatSesionId = null;

async function initChat() {
  if (!document.getElementById('chat-widget')) return;
  document.getElementById('chat-toggle').addEventListener('click', toggleChat);
  document.getElementById('chat-close').addEventListener('click', toggleChat);
  document.getElementById('chat-send').addEventListener('click', sendChat);
  document.getElementById('chat-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') sendChat();
  });
}

async function toggleChat() {
  const box = document.getElementById('chat-box');
  box.classList.toggle('open');
  if (box.classList.contains('open') && !chatSocket) {
    await startChatSession();
  }
}

async function startChatSession() {
  try {
    const data = await Chat.iniciarSesion();
    chatSesionId = data.sesion_id;
    chatSocket   = new WebSocket(`ws://localhost:8000/ws/chat/${chatSesionId}`);

    chatSocket.onmessage = e => {
      const d = JSON.parse(e.data);
      // Soporta tanto respuestas del bot como del admin
      const texto = d.respuesta || d.contenido;
      if (texto) appendChatMessage(texto, 'asistente');
    };
    chatSocket.onclose = () => {
      chatSocket = null;
      appendChatMessage('Sesión finalizada.', 'asistente');
    };
    appendChatMessage('Hola, ¿en qué te puedo ayudar? Puedes preguntarme sobre envíos, pagos, órdenes u horarios.', 'asistente');
  } catch {
    appendChatMessage('No se pudo conectar al soporte. Intenta más tarde.', 'asistente');
  }
}

function sendChat() {
  const input = document.getElementById('chat-input');
  const text  = input.value.trim();
  if (!text || !chatSocket || chatSocket.readyState !== WebSocket.OPEN) return;
  appendChatMessage(text, 'cliente');
  chatSocket.send(text);
  input.value = '';
}

function appendChatMessage(text, origen) {
  const msgs = document.getElementById('chat-messages');
  const div  = document.createElement('div');
  div.className = `chat-bubble bubble-${origen}`;
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

document.addEventListener('DOMContentLoaded', initChat);
