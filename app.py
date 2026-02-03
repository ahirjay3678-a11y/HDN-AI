import os, requests
from flask import Flask, render_template_string, request, session

API_KEY = "AIzaSyDSfNRv14gfLHV4I1WI4D2JRLoQMOGiAH0"

app = Flask(__name__)
app.secret_key = "hdn_ai_jay_31943"

def get_ai_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    context = "Tera naam HDN AI hai. Tu Jay Solanki ka assistant hai. Har bhasha mein jawab de."
    payload = {"contents": [{"parts": [{"text": f"{context}\nUser: {prompt}"}]}]}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()['candidates'][0]['content']['parts'][0]['text'].replace("\n", "<br>")
    except:
        return "Network slow hai Jay bhai, firse try karein."

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HDN AI | Jay Solanki</title>
    <style>
        body { 
            background: url('https://i.ibb.co/hR0LpXn1/1000109404.jpg') no-repeat center center fixed; 
            background-size: cover; font-family: sans-serif; height: 100vh; display: flex; flex-direction: column;
        }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: -1; }
        .header { padding: 15px; text-align: center; background: rgba(0,0,0,0.8); border-bottom: 2px solid #ff9933; color: #ff9933; }
        .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px; border-radius: 15px; font-size: 14px; color: white; }
        .user-msg { background: #ff9933; align-self: flex-end; color: black; font-weight: bold; }
        .ai-msg { background: rgba(0,0,0,0.8); align-self: flex-start; border: 1px solid #ff9933; }
        .input-area { padding: 15px; background: rgba(0,0,0,0.9); display: flex; gap: 10px; }
        input { flex: 1; background: #222; border: 1px solid #ff9933; padding: 12px; border-radius: 10px; color: white; outline: none; }
        button { background: #ff9933; color: black; border: none; padding: 0 20px; border-radius: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="overlay"></div>
    <div class="header"><h2>HDN AI 🚩</h2></div>
    <div class="chat-container" id="chat">
        {% if not session.get('name') %}
            <div class="msg ai-msg">Namaste! Main <b>HDN AI</b> hoon. Aapka naam kya hai?</div>
        {% else %}
            <div class="msg ai-msg">Swagat hai <b>{{ session['name'] }}</b>! Kuch bhi puchiye.</div>
        {% endif %}
        {% if u_msg %}
            <div class="msg user-msg">{{ u_msg }}</div>
            <div class="msg ai-msg">{{ reply | safe }}</div>
        {% endif %}
    </div>
    <form class="input-area" method="POST">
        <input type="text" name="q" placeholder="Likhein..." required>
        <button type="submit">GO</button>
    </form>
    <script>var d = document.getElementById("chat"); d.scrollTop = d.scrollHeight;</script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    reply = ""; u_msg = ""
    if request.method == 'POST':
        u_msg = request.form.get('q')
        if not session.get('name'):
            session['name'] = u_msg
            reply = f"Dhanyawad {u_msg} ji! Main taiyaar hoon."
        else:
            reply = get_ai_response(u_msg)
    return render_template_string(HTML, reply=reply, u_msg=u_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
  
