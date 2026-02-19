from flask import Flask, request, render_template_string
from deep_translator import GoogleTranslator
from collections import deque
from functools import wraps
from time import time

app = Flask(__name__)

# Store translation history (last 10 translations)
translation_history = deque(maxlen=10)

# Rate limiting decorator
def rate_limit(limit=10, per=60):
    def decorator(f):
        requests = {}
        
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            now = time()
            
            if ip in requests:
                requests[ip] = [t for t in requests[ip] if now - t < per]
                if len(requests[ip]) >= limit:
                    return "Rate limit exceeded. Please wait.", 429
                requests[ip].append(now)
            else:
                requests[ip] = [now]
                
            return f(*args, **kwargs)
        return wrapped
    return decorator

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Language Translator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-align: center;
            padding-top: 40px;
            margin: 0;
            min-height: 100vh;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        h1 {
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .translator-box {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }

        textarea {
            width: 90%;
            max-width: 500px;
            height: 120px;
            border-radius: 10px;
            border: none;
            padding: 15px;
            font-size: 16px;
            margin-bottom: 10px;
            resize: vertical;
        }

        textarea:focus {
            outline: 2px solid #667eea;
        }

        #counter {
            font-size: 14px;
            margin-bottom: 15px;
            color: #ddd;
        }

        .language-selectors {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        select, button {
            padding: 10px 15px;
            border-radius: 8px;
            border: none;
            font-size: 14px;
            cursor: pointer;
            background: white;
            color: #333;
        }

        select {
            min-width: 120px;
        }

        select:hover {
            background: #f0f0f0;
        }

        .swap-btn {
            background: #667eea;
            color: white;
            font-size: 18px;
            padding: 8px 15px;
        }

        .swap-btn:hover {
            background: #5a6fd6;
        }

        .translate-btn {
            background: #28a745;
            color: white;
            font-size: 16px;
            padding: 12px 30px;
            margin-top: 10px;
        }

        .translate-btn:hover {
            background: #218838;
        }

        .loader {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
            display: none;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .result {
            margin-top: 30px;
            font-size: 18px;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 10px;
            min-height: 50px;
        }

        .history-section {
            margin-top: 40px;
            text-align: left;
        }

        .history-title {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #fff;
        }

        .history-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .history-item strong {
            color: #ffd700;
        }

        .history-item small {
            color: #ccc;
            display: block;
            margin-top: 5px;
        }

        .error-message {
            color: #ff6b6b;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }

        footer {
            margin-top: 40px;
            font-size: 12px;
            color: #ccc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 AI Language Translator</h1>
        
        <div class="translator-box">
            <form method="POST" id="translateForm">
                <textarea name="text" id="textInput" placeholder="Enter text here..." maxlength="5000" required></textarea>
                <div id="counter">5000 characters remaining</div>
                
                <div class="language-selectors">
                    <select name="source" id="sourceLang">
                        <option value="auto">🔍 Auto Detect</option>
                        <option value="en">🇬🇧 English</option>
                        <option value="ta">🇮🇳 Tamil</option>
                        <option value="hi">🇮🇳 Hindi</option>
                        <option value="fr">🇫🇷 French</option>
                        <option value="de">🇩🇪 German</option>
                        <option value="es">🇪🇸 Spanish</option>
                        <option value="zh-CN">🇨🇳 Chinese</option>
                        <option value="ja">🇯🇵 Japanese</option>
                        <option value="ko">🇰🇷 Korean</option>
                        <option value="ru">🇷🇺 Russian</option>
                        <option value="ar">🇸🇦 Arabic</option>
                        <option value="it">🇮🇹 Italian</option>
                    </select>
                    
                    <button type="button" class="swap-btn" onclick="swapLanguages()">⇄</button>
                    
                    <select name="target" id="targetLang">
                        <option value="en">🇬🇧 English</option>
                        <option value="ta">🇮🇳 Tamil</option>
                        <option value="hi">🇮🇳 Hindi</option>
                        <option value="fr">🇫🇷 French</option>
                        <option value="de">🇩🇪 German</option>
                        <option value="es">🇪🇸 Spanish</option>
                        <option value="zh-CN">🇨🇳 Chinese</option>
                        <option value="ja">🇯🇵 Japanese</option>
                        <option value="ko">🇰🇷 Korean</option>
                        <option value="ru">🇷🇺 Russian</option>
                        <option value="ar">🇸🇦 Arabic</option>
                        <option value="it">🇮🇹 Italian</option>
                    </select>
                </div>
                
                <button type="submit" class="translate-btn">🔄 Translate</button>
            </form>
            
            <div class="loader" id="loader"></div>
            
            <div class="result" id="result">
                {{ result }}
            </div>
            
            {% if error %}
            <div class="error-message">
                ⚠️ {{ error }}
            </div>
            {% endif %}
        </div>
        
        {% if history %}
        <div class="history-section">
            <div class="history-title">📜 Recent Translations</div>
            {% for item in history %}
            <div class="history-item">
                <strong>{{ item.source|upper }} → {{ item.target|upper }}</strong><br>
                {{ item.original }}<br>
                <small>{{ item.translated }}</small>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <footer>
            Powered by Google Translator | Rate limit: 5 requests per minute
        </footer>
    </div>

    <script>
        // Character counter
        const textarea = document.getElementById('textInput');
        const counter = document.getElementById('counter');
        
        textarea.addEventListener('input', function() {
            const remaining = 5000 - this.value.length;
            counter.textContent = remaining + ' characters remaining';
            counter.style.color = remaining < 500 ? 'orange' : 'white';
        });

        // Swap languages function
        function swapLanguages() {
            const source = document.getElementById('sourceLang');
            const target = document.getElementById('targetLang');
            
            // Don't swap if source is auto-detect
            if (source.value !== 'auto') {
                [source.value, target.value] = [target.value, source.value];
            } else {
                alert('Cannot swap when source is set to Auto Detect');
            }
        }

        // Show loader on form submit
        document.getElementById('translateForm').onsubmit = function() {
            document.getElementById('loader').style.display = 'block';
            document.querySelector('.translate-btn').disabled = true;
            return true;
        };

        // Hide loader when page loads (in case of back button)
        window.onload = function() {
            document.getElementById('loader').style.display = 'none';
            document.querySelector('.translate-btn').disabled = false;
        };
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
@rate_limit(limit=5, per=60)  # 5 requests per minute
def home():
    result = ""
    error = None

    if request.method == "POST":
        text = request.form["text"]
        source = request.form["source"]
        target = request.form["target"]

        try:
            # Validate input
            if not text or len(text.strip()) == 0:
                error = "Please enter some text to translate"
            elif len(text) > 5000:
                error = "Text exceeds maximum length of 5000 characters"
            else:
                # Perform translation
                translator = GoogleTranslator(source=source, target=target)
                result = translator.translate(text)
                
                if not result or result.strip() == "":
                    error = "No translation available"
                else:
                    # Add to history
                    translation_history.appendleft({
                        'original': text[:50] + ('...' if len(text) > 50 else ''),
                        'translated': result[:50] + ('...' if len(result) > 50 else ''),
                        'source': source,
                        'target': target
                    })
        
        except Exception as e:
            error = f"Translation failed: {str(e)}"
            # Log the error for debugging
            app.logger.error(f"Translation error: {str(e)}")

    return render_template_string(
        HTML_PAGE, 
        result=result, 
        error=error, 
        history=list(translation_history)
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)