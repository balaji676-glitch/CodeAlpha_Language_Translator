from flask import Flask, request, render_template_string, send_file
from deep_translator import GoogleTranslator
from collections import deque
from functools import wraps
from time import time
import json
import os
import tempfile
from gtts import gTTS

app = Flask(__name__)

# Store translation history (last 10 translations)
translation_history = deque(maxlen=10)

# Custom Jinja2 filter for escaping JavaScript strings
@app.template_filter('tojson_safe')
def tojson_safe(s):
    """Safe JSON string escaping for JavaScript"""
    if s is None:
        return 'null'
    return json.dumps(str(s))

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

# Language to gTTS language code mapping
GTTs_LANGUAGE_MAP = {
    'ta': 'ta',  # Tamil
    'en': 'en',  # English
    'hi': 'hi',  # Hindi
    'fr': 'fr',  # French
    'de': 'de',  # German
    'es': 'es',  # Spanish
    'zh-CN': 'zh-CN',  # Chinese
    'ja': 'ja',  # Japanese
    'ko': 'ko',  # Korean
    'ru': 'ru',  # Russian
    'ar': 'ar',  # Arabic
    'it': 'it'   # Italian
}

@app.route('/speak/<lang>/<path:text>')
def speak(text, lang):
    """Generate speech using gTTS and return as audio file"""
    temp_path = None
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_path = temp_file.name
        temp_file.close()
        
        # Get language code for gTTS
        lang_code = GTTs_LANGUAGE_MAP.get(lang, 'en')
        print(f"Generating speech for language: {lang_code}, text: {text[:50]}...")  # Debug log
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(temp_path)
        
        # Send the file
        return send_file(temp_path, mimetype='audio/mpeg', as_attachment=False, download_name=f'speech_{lang}.mp3')
        
    except Exception as e:
        app.logger.error(f"gTTS error: {str(e)}")
        print(f"gTTS error details: {str(e)}")  # Debug log
        return f"Error generating speech: {str(e)}", 500
    finally:
        # Clean up temp file after sending (with a small delay to ensure file is sent)
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                app.logger.error(f"Error deleting temp file: {str(e)}")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Prime Translate - Neural Language Engine with Cloud Voice</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary: #00f3ff;
            --secondary: #ff00c3;
            --accent: #8a2be2;
            --bg-dark: #0a0a0f;
            --bg-card: rgba(20, 20, 30, 0.7);
            --text: #ffffff;
            --text-secondary: #b0b0c0;
            --neon-shadow: 0 0 10px rgba(0, 243, 255, 0.3),
                           0 0 20px rgba(0, 243, 255, 0.2),
                           0 0 30px rgba(0, 243, 255, 0.1);
            --voice-active: #00ff88;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Space Grotesk', sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
            color: var(--text);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* Animated background particles */
        body::before {
            content: '';
            position: fixed;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.1) 0%, transparent 50%);
            animation: pulse 4s ease-in-out infinite;
            pointer-events: none;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }

        /* Floating orbs */
        .orb {
            position: fixed;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.15;
            animation: float 20s infinite;
            z-index: -1;
        }

        .orb-1 {
            background: var(--primary);
            top: -100px;
            right: -100px;
            animation-delay: 0s;
        }

        .orb-2 {
            background: var(--secondary);
            bottom: -100px;
            left: -100px;
            animation-delay: -10s;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(100px, 50px) scale(1.2); }
            50% { transform: translate(50px, 100px) scale(0.8); }
            75% { transform: translate(-50px, 50px) scale(1.1); }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            position: relative;
            z-index: 1;
        }

        /* Header with neon effect */
        .header {
            text-align: center;
            margin-bottom: 60px;
            position: relative;
        }

        h1 {
            font-size: 3.5em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: var(--neon-shadow);
            margin-bottom: 10px;
            letter-spacing: 2px;
            animation: titleGlow 3s ease-in-out infinite;
            word-break: break-word;
        }

        @keyframes titleGlow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.2); }
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1em;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 5px;
            word-break: break-word;
        }

        /* Main translator card */
        .translator-card {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 32px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5),
                        0 0 0 1px rgba(0, 243, 255, 0.1) inset;
            animation: cardFloat 0.5s ease-out;
        }

        @keyframes cardFloat {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Input area */
        .input-group {
            position: relative;
            margin-bottom: 30px;
        }

        .neon-textarea {
            width: 100%;
            min-height: 160px;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(0, 243, 255, 0.3);
            border-radius: 24px;
            padding: 20px;
            color: var(--text);
            font-family: 'Space Grotesk', sans-serif;
            font-size: 16px;
            line-height: 1.6;
            resize: vertical;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.1);
        }

        .neon-textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.3);
            transform: scale(1.01);
        }

        .character-counter {
            position: absolute;
            bottom: 10px;
            right: 20px;
            background: rgba(0, 0, 0, 0.6);
            padding: 4px 12px;
            border-radius: 30px;
            font-size: 12px;
            color: var(--text-secondary);
            border: 1px solid rgba(0, 243, 255, 0.2);
            backdrop-filter: blur(5px);
        }

        /* Language selector row */
        .language-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }

        .lang-selector {
            flex: 1;
            min-width: 200px;
            position: relative;
        }

        .lang-selector label {
            display: block;
            margin-bottom: 8px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-secondary);
        }

        .neon-select {
            width: 100%;
            padding: 12px 20px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 0, 195, 0.3);
            border-radius: 16px;
            color: var(--text);
            font-family: 'Space Grotesk', sans-serif;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2300f3ff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 15px center;
            background-size: 15px;
        }

        .neon-select:focus {
            outline: none;
            border-color: var(--secondary);
            box-shadow: 0 0 30px rgba(255, 0, 195, 0.3);
        }

        .neon-select option {
            background: #1a1a2e;
            color: var(--text);
        }

        .swap-button {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
            animation: pulse 2s infinite;
        }

        .swap-button:hover {
            transform: rotate(180deg) scale(1.1);
            box-shadow: 0 0 30px rgba(255, 0, 195, 0.5);
        }

        .swap-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Translate button */
        .translate-button {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            padding: 16px 40px;
            border-radius: 40px;
            color: white;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: 30px auto 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.5);
        }

        .translate-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .translate-button:hover::before {
            left: 100%;
        }

        .translate-button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 0 40px rgba(0, 243, 255, 0.8);
        }

        .translate-button:disabled {
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }

        /* Voice status indicator and controls */
        .voice-status-container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 16px;
            padding: 15px;
            margin: 20px 0 10px 0;
            border: 1px solid var(--primary);
        }

        .voice-availability {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .voice-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .voice-badge.available {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
        }

        .voice-badge.unavailable {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid #ff0000;
            color: #ff0000;
        }

        .voice-badge.fallback {
            background: rgba(255, 165, 0, 0.2);
            border: 1px solid #ffaa00;
            color: #ffaa00;
        }

        .voice-badge.cloud {
            background: rgba(0, 243, 255, 0.2);
            border: 1px solid var(--primary);
            color: var(--primary);
        }

        .voice-test-btn {
            background: rgba(0, 243, 255, 0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
        }

        .voice-test-btn:hover:not(:disabled) {
            background: var(--primary);
            color: var(--bg-dark);
        }

        .voice-test-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }

        /* Result area with voice controls */
        .result-container {
            margin-top: 40px;
            padding: 30px;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(138, 43, 226, 0.3);
            border-radius: 24px;
            box-shadow: 0 0 30px rgba(138, 43, 226, 0.2);
            animation: glowPulse 3s infinite;
        }

        @keyframes glowPulse {
            0%, 100% { border-color: rgba(138, 43, 226, 0.3); }
            50% { border-color: rgba(0, 243, 255, 0.3); }
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .result-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-secondary);
        }

        .voice-controls {
            display: flex;
            gap: 10px;
        }

        .voice-btn {
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid var(--primary);
            color: var(--primary);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            position: relative;
            overflow: hidden;
        }

        .voice-btn:hover:not(:disabled) {
            transform: scale(1.1);
            box-shadow: 0 0 20px var(--primary);
            background: var(--primary);
            color: var(--bg-dark);
        }

        .voice-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
            border-color: var(--text-secondary);
            color: var(--text-secondary);
        }

        .voice-btn.playing {
            border-color: var(--voice-active);
            color: var(--voice-active);
            animation: soundWave 1s infinite;
        }

        .voice-btn.playing::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 2px solid var(--voice-active);
            animation: ripple 1s infinite;
        }

        @keyframes soundWave {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        @keyframes ripple {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(1.5); opacity: 0; }
        }

        .voice-btn.paused {
            border-color: #ffaa00;
            color: #ffaa00;
        }

        .result-text {
            font-size: 18px;
            line-height: 1.6;
            color: var(--text);
            word-wrap: break-word;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Voice status indicator */
        .voice-status {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 10px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--text-secondary);
            transition: all 0.3s ease;
        }

        .status-dot.active {
            background: var(--voice-active);
            box-shadow: 0 0 10px var(--voice-active);
            animation: blink 1s infinite;
        }

        .status-dot.paused {
            background: #ffaa00;
            box-shadow: 0 0 10px #ffaa00;
        }

        .status-dot.unavailable {
            background: #ff0000;
            box-shadow: 0 0 10px #ff0000;
        }

        .status-dot.cloud {
            background: var(--primary);
            box-shadow: 0 0 10px var(--primary);
            animation: cloudPulse 1.5s infinite;
        }

        @keyframes cloudPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.2); }
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Language-specific voice indicator */
        .voice-language {
            font-size: 10px;
            padding: 2px 8px;
            background: rgba(0, 243, 255, 0.1);
            border-radius: 12px;
            border: 1px solid var(--primary);
            color: var(--primary);
        }

        /* Loader */
        .cyber-loader {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1000;
        }

        .cyber-spinner {
            width: 80px;
            height: 80px;
            border: 4px solid transparent;
            border-top: 4px solid var(--primary);
            border-right: 4px solid var(--secondary);
            border-bottom: 4px solid var(--accent);
            border-left: 4px solid transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.5);
        }

        .cyber-spinner::before {
            content: '';
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            bottom: 10px;
            border: 4px solid transparent;
            border-top: 4px solid var(--secondary);
            border-right: 4px solid var(--accent);
            border-bottom: 4px solid var(--primary);
            border-left: 4px solid transparent;
            border-radius: 50%;
            animation: spin 2s linear infinite reverse;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* History section */
        .history-section {
            margin-top: 60px;
        }

        .history-title {
            font-size: 1.5em;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--primary);
            text-shadow: var(--neon-shadow);
        }

        .history-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .history-item {
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 20px;
            padding: 20px;
            transition: all 0.3s ease;
            animation: slideUp 0.5s ease-out;
            position: relative;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .history-item:hover {
            transform: translateY(-5px) scale(1.02);
            border-color: var(--secondary);
            box-shadow: 0 10px 30px rgba(255, 0, 195, 0.2);
        }

        .history-langs {
            font-size: 14px;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .history-voice-btn {
            background: none;
            border: 1px solid var(--primary);
            color: var(--primary);
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }

        .history-voice-btn:hover:not(.unavailable) {
            background: var(--primary);
            color: var(--bg-dark);
            transform: scale(1.1);
        }

        .history-voice-btn.playing {
            border-color: var(--voice-active);
            color: var(--voice-active);
            animation: soundWave 1s infinite;
        }

        .history-voice-btn.unavailable {
            border-color: #ff0000;
            color: #ff0000;
            opacity: 0.5;
            cursor: not-allowed;
        }

        .history-voice-btn.cloud {
            border-color: var(--primary);
            color: var(--primary);
            animation: cloudPulse 1.5s infinite;
        }

        .history-original {
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            word-wrap: break-word;
        }

        .history-translated {
            font-size: 16px;
            color: var(--secondary);
            font-weight: 500;
            word-wrap: break-word;
        }

        /* Error message */
        .error-message {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 0, 0, 0.1);
            border: 2px solid #ff4444;
            border-radius: 16px;
            color: #ff8888;
            text-align: center;
            backdrop-filter: blur(10px);
            animation: shake 0.5s ease-out;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }

        /* Footer */
        .footer {
            margin-top: 60px;
            text-align: center;
            font-size: 12px;
            color: var(--text-secondary);
            letter-spacing: 1px;
        }

        .neon-text {
            color: var(--primary);
            text-shadow: var(--neon-shadow);
        }

        /* Voice notification */
        .voice-notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            border: 2px solid var(--primary);
            border-radius: 16px;
            padding: 12px 20px;
            color: var(--text);
            font-size: 14px;
            transform: translateX(120%);
            transition: transform 0.3s ease;
            z-index: 1000;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.3);
        }

        .voice-notification.show {
            transform: translateX(0);
        }

        .notification-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            h1 {
                font-size: 2.2em;
                letter-spacing: 1px;
            }
            
            .subtitle {
                font-size: 0.9em;
                letter-spacing: 2px;
            }
            
            .translator-card {
                padding: 20px;
            }
            
            .language-row {
                flex-direction: column;
            }
            
            .swap-button {
                margin: 0;
                transform: rotate(90deg);
            }
            
            .swap-button:hover {
                transform: rotate(270deg) scale(1.1);
            }
            
            .history-grid {
                grid-template-columns: 1fr;
            }

            .result-header {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    
    <div class="cyber-loader" id="loader">
        <div class="cyber-spinner"></div>
    </div>

    <div class="voice-notification" id="voiceNotification">
        <div class="notification-content">
            <span id="notificationIcon">🔊</span>
            <span id="notificationMessage">Voice ready</span>
        </div>
    </div>

    <audio id="cloudAudio" style="display: none;"></audio>

    <div class="container">
        <div class="header">
            <h1>PRIME TRANSLATE</h1>
            <div class="subtitle">NEURAL LANGUAGE ENGINE WITH CLOUD VOICE</div>
        </div>

        <div class="translator-card">
            <form method="POST" id="translateForm">
                <div class="input-group">
                    <textarea name="text" class="neon-textarea" id="textInput" placeholder="Enter text to translate..." maxlength="5000" required></textarea>
                    <div class="character-counter" id="counter">5000</div>
                </div>

                <div class="language-row">
                    <div class="lang-selector">
                        <label>SOURCE LANGUAGE</label>
                        <select name="source" class="neon-select" id="sourceLang">
                            <option value="auto">🔍 AUTO DETECT</option>
                            <option value="en">🇬🇧 ENGLISH</option>
                            <option value="ta">🇮🇳 TAMIL</option>
                            <option value="hi">🇮🇳 HINDI</option>
                            <option value="fr">🇫🇷 FRENCH</option>
                            <option value="de">🇩🇪 GERMAN</option>
                            <option value="es">🇪🇸 SPANISH</option>
                            <option value="zh-CN">🇨🇳 CHINESE</option>
                            <option value="ja">🇯🇵 JAPANESE</option>
                            <option value="ko">🇰🇷 KOREAN</option>
                            <option value="ru">🇷🇺 RUSSIAN</option>
                            <option value="ar">🇸🇦 ARABIC</option>
                            <option value="it">🇮🇹 ITALIAN</option>
                        </select>
                    </div>

                    <button type="button" class="swap-button" onclick="swapLanguages()" id="swapBtn">
                        ⇄
                    </button>

                    <div class="lang-selector">
                        <label>TARGET LANGUAGE</label>
                        <select name="target" class="neon-select" id="targetLang" onchange="checkVoiceAvailability()">
                            <option value="en">🇬🇧 ENGLISH</option>
                            <option value="ta">🇮🇳 TAMIL</option>
                            <option value="hi">🇮🇳 HINDI</option>
                            <option value="fr">🇫🇷 FRENCH</option>
                            <option value="de">🇩🇪 GERMAN</option>
                            <option value="es">🇪🇸 SPANISH</option>
                            <option value="zh-CN">🇨🇳 CHINESE</option>
                            <option value="ja">🇯🇵 JAPANESE</option>
                            <option value="ko">🇰🇷 KOREAN</option>
                            <option value="ru">🇷🇺 RUSSIAN</option>
                            <option value="ar">🇸🇦 ARABIC</option>
                            <option value="it">🇮🇹 ITALIAN</option>
                        </select>
                    </div>
                </div>

                <button type="submit" class="translate-button">
                    <span>⟳ TRANSLATE</span>
                </button>
            </form>

            <!-- Voice Status Panel -->
            <div class="voice-status-container" id="voiceStatusPanel">
                <div class="voice-availability">
                    <span>🎤 Voice Support</span>
                    <span class="voice-badge" id="voiceBadge">Checking...</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <span id="voiceMessage" style="font-size: 12px; color: var(--text-secondary);">
                        Detecting available voices...
                    </span>
                    <button class="voice-test-btn" onclick="testVoice()" id="testVoiceBtn">
                        Test Voice
                    </button>
                </div>
                <div style="margin-top: 10px; font-size: 11px; color: var(--primary);" id="cloudMessage">
                    ☁️ Cloud fallback active for all languages
                </div>
            </div>

            {% if result %}
            <div class="result-container">
                <div class="result-header">
                    <div class="result-label">TRANSLATION RESULT</div>
                    <div class="voice-controls">
                        <span class="voice-language" id="targetLangDisplay">{{ target_lang|upper }}</span>
                        <button class="voice-btn" id="playBtn" onclick="togglePlay()" title="Play translation">
                            ▶️
                        </button>
                        <button class="voice-btn" id="pauseBtn" onclick="pauseSpeech()" title="Pause" disabled>
                            ⏸️
                        </button>
                        <button class="voice-btn" id="stopBtn" onclick="stopSpeech()" title="Stop">
                            ⏹️
                        </button>
                    </div>
                </div>
                <div class="result-text" id="translatedText">{{ result }}</div>
                <div class="voice-status" id="voiceStatus">
                    <span class="status-dot" id="statusDot"></span>
                    <span id="statusText">Voice ready</span>
                </div>
            </div>
            {% endif %}

            {% if error %}
            <div class="error-message">
                ⚠️ {{ error }}
            </div>
            {% endif %}
        </div>

        {% if history %}
        <div class="history-section">
            <div class="history-title">
                <span>📜 RECENT TRANSLATIONS</span>
                <span class="neon-text">({{ history|length }}/10)</span>
            </div>
            <div class="history-grid">
                {% for item in history %}
                <div class="history-item">
                    <div class="history-langs">
                        <span>{{ item.source|upper }} → {{ item.target|upper }}</span>
                        <button class="history-voice-btn" onclick='speakHistory({{ item.translated|tojson_safe|safe }}, "{{ item.target }}", this)' title="Listen to translation">
                            🔊
                        </button>
                    </div>
                    <div class="history-original">{{ item.original }}</div>
                    <div class="history-translated">{{ item.translated }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <div class="footer">
            <span class="neon-text">PRIME TRANSLATE ENGINE</span> • NEURAL NETWORK v1.0 • 5 REQ/MIN • CLOUD VOICE ENABLED
        </div>
    </div>

    <script>
        // Speech synthesis setup
        let synthesis = window.speechSynthesis;
        let currentUtterance = null;
        let isPaused = false;
        let currentPlayingElement = null;
        let availableVoices = [];
        let voiceAvailability = {};
        let useCloudVoice = true; // Start with cloud voice enabled
        const audioPlayer = document.getElementById('cloudAudio');

        // Language codes for speech with multiple fallback options
        const languageMap = {
            'en': ['en-US', 'en-GB', 'en-AU', 'en-IN', 'en'],
            'ta': ['ta-IN', 'ta-LK', 'ta-SG', 'ta-MY', 'ta'],
            'hi': ['hi-IN', 'hi'],
            'fr': ['fr-FR', 'fr-CA', 'fr-BE', 'fr-CH', 'fr'],
            'de': ['de-DE', 'de-AT', 'de-CH', 'de'],
            'es': ['es-ES', 'es-MX', 'es-AR', 'es-CO', 'es'],
            'zh-CN': ['zh-CN', 'zh-TW', 'zh-HK', 'zh'],
            'ja': ['ja-JP', 'ja'],
            'ko': ['ko-KR', 'ko'],
            'ru': ['ru-RU', 'ru'],
            'ar': ['ar-SA', 'ar-AE', 'ar-EG', 'ar'],
            'it': ['it-IT', 'it-CH', 'it']
        };

        // Show notification
        function showNotification(message, icon = '🔊') {
            const notification = document.getElementById('voiceNotification');
            const iconEl = document.getElementById('notificationIcon');
            const messageEl = document.getElementById('notificationMessage');
            
            iconEl.textContent = icon;
            messageEl.textContent = message;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }

        // Update voice status
        function updateVoiceStatus(status, type = 'ready') {
            const dot = document.getElementById('statusDot');
            const text = document.getElementById('statusText');
            
            if (dot && text) {
                dot.className = 'status-dot';
                if (type === 'playing') {
                    dot.classList.add('active');
                    text.textContent = status;
                } else if (type === 'paused') {
                    dot.classList.add('paused');
                    text.textContent = status;
                } else if (type === 'unavailable') {
                    dot.classList.add('unavailable');
                    text.textContent = status;
                } else if (type === 'cloud') {
                    dot.classList.add('cloud');
                    text.textContent = status;
                } else {
                    text.textContent = status;
                }
            }
        }

        // Load available voices
        function loadVoices() {
            availableVoices = synthesis.getVoices();
            console.log('Available voices:', availableVoices.map(v => `${v.name} (${v.lang})`));
            
            // Check voice availability for each language
            for (let lang in languageMap) {
                voiceAvailability[lang] = {
                    available: false,
                    voices: [],
                    bestMatch: null
                };
                
                // Check all variants for this language
                for (let variant of languageMap[lang]) {
                    const matchingVoices = availableVoices.filter(v => 
                        v.lang.toLowerCase().includes(variant.toLowerCase()) ||
                        variant.toLowerCase().includes(v.lang.toLowerCase())
                    );
                    
                    if (matchingVoices.length > 0) {
                        voiceAvailability[lang].available = true;
                        voiceAvailability[lang].voices.push(...matchingVoices);
                        if (!voiceAvailability[lang].bestMatch) {
                            voiceAvailability[lang].bestMatch = matchingVoices[0];
                        }
                    }
                }
            }
            
            // Check current language
            checkVoiceAvailability();
        }

        // Check if voice is available for current language
        function checkVoiceAvailability() {
            const targetLang = document.getElementById('targetLang').value;
            const voiceBadge = document.getElementById('voiceBadge');
            const voiceMessage = document.getElementById('voiceMessage');
            const testBtn = document.getElementById('testVoiceBtn');
            const playBtn = document.getElementById('playBtn');
            
            // Always use cloud voice for Tamil to ensure it works
            if (targetLang === 'ta') {
                voiceBadge.textContent = '☁️ CLOUD VOICE (ACTIVE)';
                voiceBadge.className = 'voice-badge cloud';
                voiceMessage.textContent = `☁️ Using cloud voice for Tamil (guaranteed to work)`;
                if (testBtn) testBtn.disabled = false;
                if (playBtn) playBtn.disabled = false;
                updateVoiceStatus('☁️ Cloud voice active', 'cloud');
                useCloudVoice = true;
            }
            else if (voiceAvailability[targetLang] && voiceAvailability[targetLang].available) {
                voiceBadge.textContent = '✓ VOICE AVAILABLE';
                voiceBadge.className = 'voice-badge available';
                voiceMessage.textContent = `✅ ${targetLang.toUpperCase()} voice supported (${voiceAvailability[targetLang].bestMatch.name})`;
                if (testBtn) testBtn.disabled = false;
                if (playBtn) playBtn.disabled = false;
                updateVoiceStatus('✓ Voice ready');
                useCloudVoice = false;
            } else {
                // Cloud voice is always available as fallback
                voiceBadge.textContent = '☁️ CLOUD VOICE';
                voiceBadge.className = 'voice-badge cloud';
                voiceMessage.textContent = `☁️ Using cloud voice for ${targetLang.toUpperCase()}`;
                if (testBtn) testBtn.disabled = false;
                if (playBtn) playBtn.disabled = false;
                updateVoiceStatus('☁️ Using cloud voice', 'cloud');
                useCloudVoice = true;
            }
        }

        // Test voice for current language
        async function testVoice() {
            const targetLang = document.getElementById('targetLang').value;
            const testText = targetLang === 'ta' ? 'வணக்கம்' :
                            targetLang === 'hi' ? 'नमस्ते' :
                            targetLang === 'fr' ? 'Bonjour' :
                            targetLang === 'de' ? 'Hallo' :
                            targetLang === 'es' ? 'Hola' :
                            targetLang === 'zh-CN' ? '你好' :
                            targetLang === 'ja' ? 'こんにちは' :
                            targetLang === 'ko' ? '안녕하세요' :
                            targetLang === 'ru' ? 'Привет' :
                            targetLang === 'ar' ? 'مرحبا' :
                            targetLang === 'it' ? 'Ciao' :
                            'Hello';
            
            await speakText(testText, targetLang, null, true);
        }

        // Get best available voice for language
        async function getVoiceForLanguage(langCode) {
            // First check if we already have a best match
            if (voiceAvailability[langCode] && voiceAvailability[langCode].bestMatch) {
                return voiceAvailability[langCode].bestMatch;
            }
            
            // Try all variants for this language
            const variants = languageMap[langCode] || [langCode];
            
            for (let variant of variants) {
                const voice = availableVoices.find(v => 
                    v.lang.toLowerCase() === variant.toLowerCase()
                );
                if (voice) return voice;
            }
            
            // Try partial matches
            for (let variant of variants) {
                const baseLang = variant.split('-')[0];
                const voice = availableVoices.find(v => 
                    v.lang.toLowerCase().startsWith(baseLang.toLowerCase())
                );
                if (voice) return voice;
            }
            
            return null;
        }

        // Speak text using cloud API
        async function speakCloud(text, langCode, isTest = false) {
            return new Promise((resolve, reject) => {
                // Encode the text for URL
                const encodedText = encodeURIComponent(text);
                const url = `/speak/${langCode}/${encodedText}`;
                
                console.log('Attempting cloud speech with URL:', url); // Debug log
                
                // Show loading state
                if (!isTest) {
                    updateVoiceStatus('☁️ Loading cloud voice...', 'cloud');
                }
                
                // Set up audio player event handlers
                audioPlayer.oncanplay = () => {
                    console.log('Audio can play, attempting playback...');
                    audioPlayer.play().catch(e => {
                        console.error('Playback error:', e);
                        showNotification('Playback failed: ' + e.message, '❌');
                        reject(e);
                    });
                };
                
                audioPlayer.onplay = () => {
                    console.log('Audio playing');
                    if (!isTest) {
                        updateVoiceStatus('☁️ Cloud speaking...', 'cloud');
                        showNotification(`Cloud voice for ${langCode.toUpperCase()}`, '☁️');
                    }
                    
                    if (!isTest) {
                        const playBtn = document.getElementById('playBtn');
                        const pauseBtn = document.getElementById('pauseBtn');
                        const stopBtn = document.getElementById('stopBtn');
                        
                        if (playBtn) playBtn.disabled = true;
                        if (pauseBtn) pauseBtn.disabled = true;
                        if (stopBtn) stopBtn.disabled = false;
                    }
                    
                    resolve();
                };
                
                audioPlayer.onended = () => {
                    console.log('Audio ended');
                    if (!isTest) {
                        updateVoiceStatus('✓ Voice ready');
                        showNotification('Cloud speech completed', '✅');
                        
                        const playBtn = document.getElementById('playBtn');
                        const pauseBtn = document.getElementById('pauseBtn');
                        const stopBtn = document.getElementById('stopBtn');
                        
                        if (playBtn) playBtn.disabled = false;
                        if (pauseBtn) pauseBtn.disabled = true;
                        if (stopBtn) stopBtn.disabled = true;
                    }
                    resolve();
                };
                
                audioPlayer.onerror = (e) => {
                    console.error('Audio error:', e);
                    showNotification('Cloud voice error', '❌');
                    reject(e);
                };
                
                // Set source and start loading
                audioPlayer.src = url;
                audioPlayer.load();
            });
        }

        // Speak text
        async function speakText(text, langCode, buttonElement = null, isTest = false) {
            try {
                // Stop any current speech
                stopSpeech();

                // For Tamil, always use cloud voice to ensure it works
                if (langCode === 'ta') {
                    useCloudVoice = true;
                }
                
                if (useCloudVoice) {
                    // Use cloud voice
                    await speakCloud(text, langCode, isTest);
                    
                    if (buttonElement) {
                        buttonElement.classList.add('cloud');
                        currentPlayingElement = buttonElement;
                    }
                    
                } else {
                    // Use browser's speech synthesis
                    const voice = await getVoiceForLanguage(langCode);
                    
                    if (!voice) {
                        // Fallback to cloud
                        console.log('No voice found, falling back to cloud');
                        useCloudVoice = true;
                        await speakCloud(text, langCode, isTest);
                        return;
                    }

                    // Create utterance
                    currentUtterance = new SpeechSynthesisUtterance(text);
                    currentUtterance.voice = voice;
                    currentUtterance.lang = voice.lang;
                    currentUtterance.rate = 1.0;
                    currentUtterance.pitch = 1.0;
                    currentUtterance.volume = 1.0;

                    // Event handlers
                    currentUtterance.onstart = () => {
                        updateVoiceStatus(isTest ? '🔊 Testing voice...' : '🔊 Speaking...', 'playing');
                        if (buttonElement) {
                            buttonElement.classList.add('playing');
                            currentPlayingElement = buttonElement;
                        }
                        
                        const playBtn = document.getElementById('playBtn');
                        const pauseBtn = document.getElementById('pauseBtn');
                        const stopBtn = document.getElementById('stopBtn');
                        
                        if (playBtn && !isTest) playBtn.disabled = true;
                        if (pauseBtn && !isTest) pauseBtn.disabled = false;
                        if (stopBtn && !isTest) stopBtn.disabled = false;
                        
                        showNotification(isTest ? `Testing ${langCode.toUpperCase()} voice` : `Speaking in ${langCode.toUpperCase()}`, '🔊');
                    };

                    currentUtterance.onpause = () => {
                        updateVoiceStatus('⏸️ Paused', 'paused');
                        const pauseBtn = document.getElementById('pauseBtn');
                        if (pauseBtn) pauseBtn.classList.add('paused');
                    };

                    currentUtterance.onresume = () => {
                        updateVoiceStatus('🔊 Speaking...', 'playing');
                        const pauseBtn = document.getElementById('pauseBtn');
                        if (pauseBtn) pauseBtn.classList.remove('paused');
                    };

                    currentUtterance.onend = () => {
                        if (!isTest) {
                            updateVoiceStatus('✓ Voice ready');
                        } else {
                            checkVoiceAvailability();
                        }
                        
                        if (buttonElement) {
                            buttonElement.classList.remove('playing');
                        }
                        if (currentPlayingElement) {
                            currentPlayingElement.classList.remove('playing');
                        }
                        
                        const playBtn = document.getElementById('playBtn');
                        const pauseBtn = document.getElementById('pauseBtn');
                        const stopBtn = document.getElementById('stopBtn');
                        
                        if (playBtn && !isTest) playBtn.disabled = false;
                        if (pauseBtn && !isTest) {
                            pauseBtn.disabled = true;
                            pauseBtn.classList.remove('paused');
                        }
                        if (stopBtn && !isTest) stopBtn.disabled = true;
                        
                        currentPlayingElement = null;
                        showNotification(isTest ? 'Voice test completed' : 'Speech completed', '✅');
                    };

                    currentUtterance.onerror = (event) => {
                        console.error('Speech error:', event);
                        
                        // Fallback to cloud on error
                        showNotification('System voice failed, trying cloud...', '⚠️');
                        useCloudVoice = true;
                        speakCloud(text, langCode, isTest);
                    };

                    // Start speaking
                    synthesis.speak(currentUtterance);
                }

            } catch (error) {
                console.error('Speech synthesis error:', error);
                showNotification('Voice error: ' + error.message, '❌');
            }
        }

        // Toggle play/pause
        function togglePlay() {
            if (useCloudVoice) {
                // Cloud voice doesn't support pause, just play/stop
                if (audioPlayer.paused) {
                    const text = document.getElementById('translatedText').textContent;
                    const lang = document.getElementById('targetLang').value;
                    speakText(text, lang, document.getElementById('playBtn'));
                } else {
                    audioPlayer.pause();
                    showNotification('Paused', '⏸️');
                }
            } else if (!currentUtterance) {
                // Play new speech
                const text = document.getElementById('translatedText').textContent;
                const lang = document.getElementById('targetLang').value;
                speakText(text, lang, document.getElementById('playBtn'));
            } else if (isPaused) {
                // Resume
                synthesis.resume();
                isPaused = false;
                updateVoiceStatus('🔊 Speaking...', 'playing');
                
                const playBtn = document.getElementById('playBtn');
                const pauseBtn = document.getElementById('pauseBtn');
                
                if (playBtn) playBtn.disabled = true;
                if (pauseBtn) {
                    pauseBtn.disabled = false;
                    pauseBtn.classList.remove('paused');
                }
                
                showNotification('Resumed', '▶️');
            }
        }

        // Pause speech
        function pauseSpeech() {
            if (!useCloudVoice && synthesis.speaking && !synthesis.paused) {
                synthesis.pause();
                isPaused = true;
                updateVoiceStatus('⏸️ Paused', 'paused');
                
                const playBtn = document.getElementById('playBtn');
                const pauseBtn = document.getElementById('pauseBtn');
                
                if (playBtn) playBtn.disabled = false;
                if (pauseBtn) pauseBtn.disabled = true;
                
                showNotification('Paused', '⏸️');
            }
        }

        // Stop speech
        function stopSpeech() {
            if (useCloudVoice) {
                audioPlayer.pause();
                audioPlayer.currentTime = 0;
                audioPlayer.src = '';
                updateVoiceStatus('✓ Voice ready');
                
                const playBtn = document.getElementById('playBtn');
                const pauseBtn = document.getElementById('pauseBtn');
                const stopBtn = document.getElementById('stopBtn');
                
                if (playBtn) playBtn.disabled = false;
                if (pauseBtn) {
                    pauseBtn.disabled = true;
                    pauseBtn.classList.remove('paused');
                }
                if (stopBtn) stopBtn.disabled = true;
                
                // Remove playing class from any element
                if (currentPlayingElement) {
                    currentPlayingElement.classList.remove('cloud');
                }
                document.querySelectorAll('.history-voice-btn').forEach(btn => {
                    btn.classList.remove('cloud');
                    btn.classList.remove('playing');
                });
                
                showNotification('Stopped', '⏹️');
            } else if (synthesis.speaking || synthesis.paused) {
                synthesis.cancel();
                currentUtterance = null;
                isPaused = false;
                updateVoiceStatus('✓ Voice ready');
                
                const playBtn = document.getElementById('playBtn');
                const pauseBtn = document.getElementById('pauseBtn');
                const stopBtn = document.getElementById('stopBtn');
                
                if (playBtn) playBtn.disabled = false;
                if (pauseBtn) {
                    pauseBtn.disabled = true;
                    pauseBtn.classList.remove('paused');
                }
                if (stopBtn) stopBtn.disabled = true;
                
                // Remove playing class from any element
                if (currentPlayingElement) {
                    currentPlayingElement.classList.remove('playing');
                }
                document.querySelectorAll('.history-voice-btn').forEach(btn => {
                    btn.classList.remove('playing');
                });
                
                showNotification('Stopped', '⏹️');
            }
        }

        // Speak from history
        function speakHistory(text, langCode, button) {
            // Remove playing class from all history buttons
            document.querySelectorAll('.history-voice-btn').forEach(btn => {
                btn.classList.remove('playing');
                btn.classList.remove('cloud');
            });
            
            speakText(text, langCode, button);
        }

        // Character counter
        const textarea = document.getElementById('textInput');
        const counter = document.getElementById('counter');
        const maxLength = 5000;
        
        if (textarea) {
            textarea.addEventListener('input', function() {
                const remaining = maxLength - this.value.length;
                counter.textContent = remaining;
                
                if (remaining < 500) {
                    counter.style.color = '#ff00c3';
                    counter.style.textShadow = '0 0 10px #ff00c3';
                } else if (remaining < 1000) {
                    counter.style.color = '#ffaa00';
                    counter.style.textShadow = '0 0 10px #ffaa00';
                } else {
                    counter.style.color = '#00f3ff';
                    counter.style.textShadow = '0 0 10px #00f3ff';
                }
                
                counter.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    counter.style.transform = 'scale(1)';
                }, 100);
            });
        }

        // Swap languages
        function swapLanguages() {
            const source = document.getElementById('sourceLang');
            const target = document.getElementById('targetLang');
            const swapBtn = document.getElementById('swapBtn');
            
            if (source.value !== 'auto') {
                swapBtn.style.transform = 'rotate(180deg) scale(1.2)';
                setTimeout(() => {
                    [source.value, target.value] = [target.value, source.value];
                    swapBtn.style.transform = '';
                    checkVoiceAvailability();
                }, 150);
            } else {
                swapBtn.style.backgroundColor = '#ff4444';
                swapBtn.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    swapBtn.style.backgroundColor = '';
                    swapBtn.style.transform = '';
                }, 300);
                alert('Cannot swap when source is set to Auto Detect');
            }
        }

        // Form submit
        const translateForm = document.getElementById('translateForm');
        if (translateForm) {
            translateForm.onsubmit = function() {
                const loader = document.getElementById('loader');
                const button = document.querySelector('.translate-button');
                
                loader.style.display = 'block';
                button.disabled = true;
                button.style.opacity = '0.7';
                document.body.style.overflow = 'hidden';
                
                return true;
            };
        }

        // Page load
        window.onload = function() {
            const loader = document.getElementById('loader');
            const button = document.querySelector('.translate-button');
            
            if (loader) loader.style.display = 'none';
            if (button) {
                button.disabled = false;
                button.style.opacity = '';
            }
            document.body.style.overflow = '';
            
            if (counter) {
                counter.style.color = '#00f3ff';
                counter.style.textShadow = '0 0 10px #00f3ff';
            }
            
            // Initialize speech synthesis
            if (synthesis) {
                if (synthesis.onvoiceschanged !== undefined) {
                    synthesis.onvoiceschanged = loadVoices;
                }
                loadVoices();
            }
            
            // Always enable cloud voice as fallback
            useCloudVoice = true;
            showNotification('Cloud voice ready for all languages', '☁️');

            // Update target language display
            const targetLang = document.getElementById('targetLang');
            const targetDisplay = document.getElementById('targetLangDisplay');
            if (targetLang && targetDisplay) {
                targetDisplay.textContent = targetLang.value.toUpperCase();
            }
            
            // Check voice availability
            checkVoiceAvailability();
        };

        // Update target language display when changed
        const targetLang = document.getElementById('targetLang');
        if (targetLang) {
            targetLang.addEventListener('change', function() {
                const display = document.getElementById('targetLangDisplay');
                if (display) {
                    display.textContent = this.value.toUpperCase();
                }
                // Stop any ongoing speech when language changes
                stopSpeech();
                // Check voice availability
                checkVoiceAvailability();
            });
        }

        // Handle page unload
        window.onbeforeunload = function() {
            if (synthesis && synthesis.speaking) {
                synthesis.cancel();
            }
            if (audioPlayer) {
                audioPlayer.pause();
                audioPlayer.src = '';
            }
        };

        // Console easter egg
        console.log('%c⚡ PRIME TRANSLATE ENGINE WITH CLOUD VOICE ⚡', 'color: #00f3ff; font-size: 16px; font-weight: bold; text-shadow: 0 0 10px #00f3ff');
        console.log('%cNeural Network Status: ONLINE', 'color: #00ff00');
        console.log('%cCloud Voice: ENABLED for all languages', 'color: #ff00c3');
        console.log('%cTamil Voice: Using CLOUD backup', 'color: #8a2be2');

        // Hover effects
        document.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('mousemove', (e) => {
                const rect = item.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                item.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(0,243,255,0.2), rgba(0,0,0,0.4))`;
            });
            
            item.addEventListener('mouseleave', () => {
                item.style.background = '';
            });
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
@rate_limit(limit=5, per=60)  # 5 requests per minute
def home():
    result = ""
    error = None
    target_lang = "en"  # Default target language

    if request.method == "POST":
        text = request.form["text"]
        source = request.form["source"]
        target = request.form["target"]
        target_lang = target

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
        history=list(translation_history),
        target_lang=target_lang
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)