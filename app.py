from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import json
import os

app = Flask(__name__)
CORS(app)

# Senin API Anahtarın buraya eklendi
API_KEY = "AIzaSyDWOAHem4YzQhs2p0-pvRXQ2r5qWslGUmI"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "ARDA AI Sunucusu Aktif!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    try:
        req = urllib.request.Request(
            URL, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            
    except Exception as e:
        ai_reply = f"Hata olustu: {str(e)}"
        
    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    # Render sistemine uygun port ayarı
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
