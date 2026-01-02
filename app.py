import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN DEBUG TERMINAL</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --green: #00ff41; --cyan: #00f3ff; --red: #ff003c; --bg: #020202; }
        body { background: var(--bg); color: var(--cyan); font-family: 'Consolas', monospace; margin: 0; height: 100vh; display: flex; flex-direction: column; }
        
        .header { background: #111; padding: 10px; border-bottom: 2px solid var(--cyan); text-align: center; font-weight: bold; font-size: 14px; }

        .main-layout { display: flex; flex: 1; overflow: hidden; }
        
        /* Control Panel */
        .controls { width: 300px; padding: 15px; background: #080808; border-right: 1px solid #222; overflow-y: auto; }
        input { width: 100%; padding: 10px; margin: 5px 0 15px 0; background: #000; border: 1px solid #333; color: var(--cyan); font-size: 12px; }
        button { width: 100%; padding: 12px; background: var(--cyan); color: #000; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { opacity: 0.8; box-shadow: 0 0 15px var(--cyan); }

        /* Debug Terminal */
        .terminal-container { flex: 1; display: flex; flex-direction: column; background: #000; }
        .terminal { flex: 1; overflow-y: scroll; padding: 10px; font-size: 12px; line-height: 1.5; scroll-behavior: smooth; }
        
        /* Message Types */
        .line { margin-bottom: 8px; word-break: break-all; border-left: 3px solid #333; padding-left: 8px; }
        .in { color: var(--green); border-color: var(--green); } /* Incoming Payloads */
        .out { color: var(--cyan); border-color: var(--cyan); } /* Outgoing Payloads */
        .err { color: var(--red); border-color: var(--red); }
        .sys { color: #888; border-color: #444; }
        
        .timestamp { color: #555; font-size: 10px; margin-right: 5px; }
        
        /* Custom Scrollbar */
        .terminal::-webkit-scrollbar { width: 8px; }
        .terminal::-webkit-scrollbar-track { background: #050505; }
        .terminal::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
        .terminal::-webkit-scrollbar-thumb:hover { background: #333; }
    </style>
</head>
<body>
    <div class="header">TITAN_DEBUG_TERMINAL_v3.1 [LOGGING_ENABLED]</div>
    
    <div class="main-layout">
        <div class="controls">
            <label>BOT CREDENTIALS</label>
            <input type="text" id="user" placeholder="Username">
            <input type="password" id="pass" placeholder="Password">
            
            <label>TEST TARGET</label>
            <input type="text" id="room" placeholder="Room Name">
            <input type="text" id="target" placeholder="Target ID">
            
            <button onclick="initBot()">START DEBUGGER</button>
            <button onclick="clearTerminal()" style="margin-top:10px; background:#333; color:#fff;">CLEAR LOGS</button>
        </div>

        <div class="terminal-container">
            <div id="terminal" class="terminal">
                <div class="line sys">Initializing Debug Environment... Waiting for user.</div>
            </div>
        </div>
    </div>

    <script>
        let ws;
        const terminal = document.getElementById('terminal');

        function log(msg, type='sys') {
            const time = new Date().toLocaleTimeString();
            const div = document.createElement('div');
            div.className = `line ${type}`;
            div.innerHTML = `<span class="timestamp">[${time}]</span><b>${type.toUpperCase()}:</b> ${msg}`;
            terminal.appendChild(div);
            
            // Auto-scroll logic
            terminal.scrollTop = terminal.scrollHeight;
        }

        function clearTerminal() { terminal.innerHTML = '<div class="line sys">Terminal cleared.</div>'; }

        function initBot() {
            const u = document.getElementById('user').value;
            const p = document.getElementById('pass').value;
            const r = document.getElementById('room').value;
            const t = document.getElementById('target').value;

            if(!u || !p) { log("Error: Credentials missing", "err"); return; }

            ws = new WebSocket("wss://chatp.net:5333/server");

            ws.onopen = () => {
                log("Connection Established. Sending Login Packet...", "sys");
                const loginPacket = {handler:"login", id: Math.random(), username: u, password: p};
                ws.send(JSON.stringify(loginPacket));
                log(JSON.stringify(loginPacket), "out");
            };

            ws.onmessage = (e) => {
                // LOG EVERY INCOMING PAYLOAD
                log(e.data, "in");

                const data = JSON.parse(e.data);

                // Handle Login
                if(data.handler === "login_event" && data.type === "success") {
                    log("Login Verified. Joining Room: " + r, "sys");
                    ws.send(JSON.stringify({handler:"room_join", id: Math.random(), name: r}));
                }

                // Auto-Fire Stability Test on Room Joined
                if(data.handler === "room_event" && data.type === "room_joined") {
                    log("Joined Room. Preparing Diagnostic Payloads...", "sys");
                    
                    const payload = "జ్ఞा" + " ҉ ".repeat(15) + "ဪ".repeat(5);
                    const msgPacket = {
                        handler: "chat_message",
                        to: t,
                        type: "text",
                        body: payload
                    };
                    
                    log("Firing Stability Packet to " + t, "sys");
                    ws.send(JSON.stringify(msgPacket));
                    log(JSON.stringify(msgPacket), "out");
                }
            };

            ws.onclose = () => log("WebSocket Disconnected.", "err");
            ws.onerror = () => log("WebSocket Connection Error!", "err");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
