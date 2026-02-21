# 🌍 Prime Translate - AI Language Translation Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/balaji676-glitch/CodeAlpha_Language_Translator)

<div align="center">
  <img src="https://via.placeholder.com/800x400/0a0a0f/00f3ff?text=Prime+Translate+Demo" alt="Project Demo Screenshot">
  <p><i>✨ Cyberpunk-themed AI Translation with Voice Support ✨</i></p>
</div>

## 🚀 Project Overview

**Prime Translate** is an AI-powered language translation tool developed during my internship at **CodeAlpha** (Task 1). This web application breaks language barriers by providing instant translations across 12+ languages with a stunning cyberpunk-inspired interface and cloud-based voice synthesis.

🔗 **Live Demo**: *[Add your deployment link here if available]*  
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