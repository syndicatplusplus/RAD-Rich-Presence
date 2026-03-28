# 🎮 RAD Rich Presence

A lightweight desktop app that displays your **RetroAchievements activity** as a **Discord Rich Presence**.

<table>
  <tr>
    <td align="center">
      <img src="assets/new_achievement.gif" width="370"/>
    </td>
    <td align="center">
      <img src="assets/achievement_update.gif" width="370"/>
    </td>
  </tr>
</table>

Shows:

* 🎮 What you're currently playing
* 🏆 Your most recent achievement
* 🖼 Game artwork
* ⏱ Session timer

Runs quietly in the system tray and updates automatically.

---

## ✨ Features

* Discord Rich Presence integration
* Displays current game + console
* Shows most recent achievement (with fallback if API hiccups)
* Uses official RetroAchievements API
* System tray app (no terminal window)
* Configurable polling interval
* Clean and minimal UI

---

## 🧰 Requirements

* Python 3.8+
* Discord (running in the background)
* RetroAchievements account + API key

---

## ⚙️ Setup (Run from Python)

### 1. Clone the repository

```bash
git clone https://github.com/syndicatplusplus/RAD-Rich-Presence.git
cd RADRichPresence
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment

Copy the example config:

```bash
copy .env.example .env
```

Then open `.env` and fill in your values:

```text
RA_USERNAME=your_username_here
RA_API_KEY=your_api_key_here
DISCORD_CLIENT_ID=your_discord_client_id
POLL_SECONDS=120
```

---

### 4. Run the app

```bash
python rad_rich_presence.py
```

You should see a tray icon appear, and your Discord status will update.

---

## 🖥️ Build the Executable (.exe)

### Build using PyInstaller

```bash
py -m PyInstaller --noconfirm --onedir --noconsole --name RADRichPresence rad_rich_presence.py
```

---

### After building

Navigate to:

```text
dist/RADRichPresence/
```

Then copy these files into that folder:

```text
.env
ra_logo.png
```

Final structure should look like:

```text
RADRichPresence/
├── RADRichPresence.exe
├── .env
├── ra_logo.png
```

---

### Run the app

Double-click:

```text
RADRichPresence.exe
```

The app will run in the system tray.

---

## ⚠️ Important Notes

* The `.env` file is required — the app will not run without it
* Do NOT share your `.env` file (it contains your API key)
* The `dist/` folder is rebuilt each time you build — you must re-copy `.env` and `ra_logo.png`

---

## 🧪 Troubleshooting

### App opens and immediately closes

* `.env` is missing or invalid
* Make sure it is next to the `.exe`

---

### Discord status not updating

* Ensure Discord is running
* Check your `DISCORD_CLIENT_ID`
* Verify your RetroAchievements API key

---

### Achievement not updating immediately

* The app polls the API at intervals (`POLL_SECONDS`)
* Default is 120 seconds to avoid rate limits

---

## 🧠 How It Works

* Polls RetroAchievements API for:

  * current game
  * recent achievements
* Tracks state changes to avoid unnecessary updates
* Sends updates to Discord via local IPC (pypresence)
* Runs as a background thread with a system tray interface

---

## 📦 Dependencies

* requests
* python-dotenv
* pypresence
* pystray
* pillow

---

## 📜 License

MIT License

---

## 🙌 Credits

* RetroAchievements API
* Discord Rich Presence
* Python for being comfy and easy to use
