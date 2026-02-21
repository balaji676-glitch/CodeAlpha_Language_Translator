# 🌍 Prime Translate - AI Language Translation Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/balaji676-glitch/CodeAlpha_Language_Translator)

<div align="center">
 
  <p><i>✨ Cyberpunk-themed AI Translation with Voice Support ✨</i></p>
</div>

## 🚀 Project Overview

**Prime Translate** is an AI-powered language translation tool developed during my internship at **CodeAlpha** (Task 1). This web application breaks language barriers by providing instant translations across 12+ languages with a stunning cyberpunk-inspired interface and cloud-based voice synthesis.


📦 **Repository**: [github.com/balaji676-glitch/CodeAlpha_Language_Translator](https://github.com/balaji676-glitch/CodeAlpha_Language_Translator)

---

## ✨ Key Features

### 🌐 **Multi-Language Support** (12+ Languages)
| Language | Code | Support |
|----------|------|---------|
| 🇬🇧 English | `en` | ✅ Full |
| 🇮🇳 Tamil | `ta` | ✅ Full + Voice |
| 🇮🇳 Hindi | `hi` | ✅ Full |
| 🇫🇷 French | `fr` | ✅ Full |
| 🇩🇪 German | `de` | ✅ Full |
| 🇪🇸 Spanish | `es` | ✅ Full |
| 🇨🇳 Chinese | `zh-CN` | ✅ Full |
| 🇯🇵 Japanese | `ja` | ✅ Full |
| 🇰🇷 Korean | `ko` | ✅ Full |
| 🇷🇺 Russian | `ru` | ✅ Full |
| 🇸🇦 Arabic | `ar` | ✅ Full |
| 🇮🇹 Italian | `it` | ✅ Full |
| 🔍 Auto-detect | `auto` | ✅ Available |

### 🎤 **Advanced Voice Assistant**
- **Dual-mode voice system**: Browser speech synthesis + Cloud fallback (gTTS)
- **Tamil voice support** even without system voices
- Complete playback controls: Play ▶️ | Pause ⏸️ | Stop ⏹️
- Voice test feature for each language
- Real-time voice status indicators
- History items with voice playback

### ⚡ **Powerful Features**
- **5000-character limit** with real-time counter
- **Translation history** (last 10 translations)
- **One-click language swap** (with auto-detect protection)
- **Rate limiting**: 5 requests per minute
- **Input validation** and error handling
- **Copy functionality** via history items

### 🎨 **Unique UI/UX Design**
- Cyberpunk neon theme with gradient effects
- Glass morphism cards with backdrop blur
- Floating animated background orbs
- Smooth hover animations and transitions
- Fully responsive for mobile devices
- Real-time visual feedback for all actions

---

## 🛠️ **Technologies Used**

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.8+, Flask |
| **Translation** | GoogleTranslator API (via `deep-translator`) |
| **Voice (Cloud)** | Google Text-to-Speech (`gTTS`) |
| **Voice (Browser)** | Web Speech API |
| **Frontend** | HTML5, CSS3, JavaScript (ES6) |
| **Security** | Rate limiting, Input sanitization |
| **Version Control** | Git, GitHub |

---

## 📦 **Installation & Setup**

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/balaji676-glitch/CodeAlpha_Language_Translator.git
   cd CodeAlpha_Language_Translator

🎯 How to Use
  Enter text in the input area (max 5000 characters)
  
  Select languages:
  
  Source language (or choose "Auto Detect")
  
  Target language for translation
  
  Click "TRANSLATE" to get instant translation
  
  Listen to translation:
  
  Click ▶️ to hear the translated text
  
  Use ⏸️ to pause, ⏹️ to stop
  
  "Test Voice" button to check language support
  
  View history below for recent translations
  
  Click history voice button 🔊 to replay any translation

📁 Project Structure
  CodeAlpha_Language_Translator/
│
├── app.py                 # Main Flask application
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
│
└── (Optional folders)
    ├── static/            # CSS, JS, images (if separated)
    └── templates/         # HTML templates (if separated)


🧠 Key Learning Outcomes
  ✅ Integrating third-party APIs (Google Translate, gTTS)
  
  ✅ Building fallback mechanisms for better user experience
  
  ✅ Creating responsive, visually appealing UIs with CSS
  
  ✅ Implementing rate limiting for API protection
  
  ✅ Handling multilingual text and special characters
  
  ✅ Working with browser's Web Speech API
  
  ✅ Error handling and user feedback systems
  
  ✅ Version control with Git/GitHub

🚦 API Rate Limits
  Translation: 5 requests per minute per IP
  
  Voice: Cloud fallback uses gTTS (no rate limits)
  
  Input validation prevents abuse

🤝 Contributing
  Contributions, issues, and feature requests are welcome!
  
  Fork the project
  
  Create your feature branch (git checkout -b feature/AmazingFeature)
  
  Commit your changes (git commit -m 'Add some AmazingFeature')
  
  Push to the branch (git push origin feature/AmazingFeature)
  
  Open a Pull Request

📝 License
  This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
  Balaji
  Artificial Intelligence Intern at CodeAlpha
  
🙏 Acknowledgments
  CodeAlpha for the internship opportunity and guidance
  
  Google Translate API for translation services
  
  gTTS for cloud-based voice synthesis
  
  Flask community for excellent documentation

📊 Repository Stats
  https://img.shields.io/github/last-commit/balaji676-glitch/CodeAlpha_Language_Translator
  https://img.shields.io/github/issues/balaji676-glitch/CodeAlpha_Language_Translator
  https://img.shields.io/github/stars/balaji676-glitch/CodeAlpha_Language_Translator?style=social
  
  <div align="center"> <h3>⭐ Star this repository if you find it useful! ⭐</h3> <p>Built with ❤️ during CodeAlpha Internship</p> </div>
  #CodeAlpha #Python #Flask #AI #LanguageTranslation #VoiceTechnology #MachineLearning #WebDevelopment #TamilNLP
