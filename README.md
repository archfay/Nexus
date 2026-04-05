<div align="center">
  <img src="https://github.com/hikariatama/assets/raw/master/1326-command-window-line-flat.webp" height="100" alt="Nexus Logo">
  
  # 🚀 Nexus Userbot
  
  **Advanced Telegram userbot with enhanced security and modern features**
  
  [![Codacy Grade](https://app.codacy.com/project/badge/Grade/97e3ea868f9344a5aa6e4d874f83db14)](https://www.codacy.com/gh/archfay/Nexus)
  [![Code Size](https://img.shields.io/github/languages/code-size/archfay/Nexus?color=blue)](https://github.com/archfay/Nexus)
  [![Issues](https://img.shields.io/github/issues-raw/archfay/Nexus?color=red)](https://github.com/archfay/Nexus/issues)
  [![License](https://img.shields.io/github/license/archfay/Nexus?color=green)](LICENSE)
  [![Commit Activity](https://img.shields.io/github/commit-activity/m/archfay/Nexus?color=orange)](https://github.com/archfay/Nexus)
  [![Stars](https://img.shields.io/github/stars/archfay/Nexus?style=flat&color=yellow)](https://github.com/archfay/Nexus/stargazers)
  [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  
  [📖 Documentation](#-documentation) • [🔧 Installation](#-installation) • [✨ Features](#-features) • [💬 Support](#-support)
</div>

---

## ⚠️ Security Notice

> **Important Security Advisory**
> 
> While Nexus implements extended security measures, installing modules from untrusted developers may still cause damage to your server/account.
> 
> **Best Practices:**
> - ✅ Download modules exclusively from official repositories or trusted developers
> - ✅ Enable `.api_fw_protection` for additional security
> - ❌ Do NOT install modules if unsure about their safety
> - ⚠️ Exercise caution with powerful commands (`.terminal`, `.eval`, `.ecpp`, etc.)
> - ⚠️ Avoid installing many modules at once

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9 - 3.13**
- **Git** (for version control)
- **Telegram API Credentials** from [Telegram Apps](https://my.telegram.org/apps)

### Installation

#### One-liner (Linux/macOS)
```bash
apt update && apt install git python3 -y && \
git clone https://github.com/archfay/Nexus && \
cd Nexus && \
pip install -r requirements.txt && \
python3 -m nexus
```

#### Step-by-step
```bash
# Clone repository
git clone https://github.com/archfay/Nexus
cd Nexus

# Install dependencies
pip install -r requirements.txt

# Run Nexus
python3 -m nexus
```

#### VPS/VDS Options
```bash
python3 -m nexus --proxy-pass    # Enable SSH tunneling
python3 -m nexus --no-web        # Console-only setup
python3 -m nexus --root          # For root users (skip force_insecure)
```

#### Docker
```bash
docker-compose up -d
# or
bash docker.sh
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🆕 **Latest Telegram Layer** | Support for forums and newest Telegram features |
| 🔒 **Enhanced Security** | Native entity caching and targeted security rules |
| 🎨 **Modern UI/UX** | Intuitive interface and smooth user experience |
| 📦 **Rich Core Modules** | Improved and new core functionality |
| ⚡ **Rapid Bug Fixes** | Faster resolution than FTG/GeekTG |
| 🔄 **Full Compatibility** | Works with FTG, GeekTG and Hikka modules |
| ▶️ **Inline Elements** | Forms, galleries, lists and interactive elements |
| 🌍 **Multi-language** | Support for EN, RU, DE, UA |
| 💾 **Auto Backup** | Automatic database backups |
| 🔐 **API Protection** | Built-in API firewall protection |

---

## 📚 Documentation

| Resource | Link |
|----------|------|
| **User Guide** | [nexus-ub.xyz](https://nexus-ub.xyz/) |
| **Developer Docs** | [dev.nexus-ub.xyz](https://dev.nexus-ub.xyz/) |
| **GitHub Issues** | [Report bugs](https://github.com/archfay/Nexus/issues) |

---

## 📦 Core Modules

Nexus comes with powerful built-in modules:

- **Terminal** - Execute system commands
- **Eval** - Python code execution
- **Loader** - Module management
- **Updater** - Auto-update functionality
- **Settings** - User preferences
- **Help** - Command documentation
- **Backup** - Database backups
- **Security** - Enhanced protection
- **Web** - Web interface
- **Inline** - Interactive elements

---

## 🛠️ Development

### Project Structure
```
Nexus/
├── nexus/              # Main package
│   ├── modules/        # Core modules
│   ├── inline/         # Inline handlers
│   ├── web/            # Web interface
│   ├── secure/         # Security features
│   └── langpacks/      # Translations
├── web-resources/      # Web assets
├── loaded_modules/     # User modules
└── requirements.txt    # Dependencies
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 💬 Support

[![Telegram Support](https://img.shields.io/badge/Telegram-Support_Group-2594cb?logo=telegram&style=for-the-badge)](https://t.me/Nexus_Talking)

Join our community for:
- 💡 Tips and tricks
- 🐛 Bug reports
- 💬 General discussion
- 📢 Announcements

---

## ⚖️ Legal Disclaimer

> This project is provided **as-is** without any warranty. The developer takes **NO responsibility** for:
> - Account bans or restrictions from Telegram
> - Message deletions or content moderation
> - Security issues from third-party modules
> - Session leaks from malicious modules
> - Any other damages or losses
>
> **Always review [Telegram's Terms of Service](https://core.telegram.org/api/terms) before use.**

---

## 📄 License

This project is licensed under the **GNU AGPLv3** License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgements

- **[Hikari](https://gitlab.com/hikariatama)** - For Hikka (project foundation)
- **[Lonami](https://t.me/lonami)** - For Telethon (Nexus-TL backbone)
- **[DoNotWeb](https://github.com/DoNotWeb)** - Current maintainer

---

<div align="center">
  
  **Made with ❤️ by the Nexus Community**
  
  [⬆ Back to top](#-nexus-userbot)
  
</div>
