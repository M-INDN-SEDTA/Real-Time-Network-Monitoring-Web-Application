# Youtube Comments, Description, Related, Playlist Right/Side Panel  

![Status](https://img.shields.io/badge/status-active-success) ![Firefox](https://img.shields.io/badge/firefox-supported-orange?logo=firefox) ![Chrome](https://img.shields.io/badge/chrome-supported-green?logo=google-chrome) ![Edge](https://img.shields.io/badge/edge-supported-blue?logo=microsoft-edge) ![License](https://img.shields.io/badge/license-MIT-blue) ![MadeWith](https://img.shields.io/badge/made%20with-JavaScript-yellow?logo=javascript)

> A lightweight browser extension that adds a **right-hand sidebar with tabs** for YouTube.  
> Quickly switch between **Comments, Description, Related Videos, and Playlist** — all in one panel.  

<p align="center">
  <img src="assets/demo.gif" alt="Extension Demo" width="720px">
</p>  

---

## ✨ Features
- 📑 **Tabbed Sidebar** → Comments, Description, Related, Playlist (auto-detected).  
- 🎨 Matches YouTube’s dark & light themes seamlessly.  
- ⚡ Instant — no page reloads, no external requests, no tracking.  
- 📺 Playlist-aware → adds Playlist tab only when available.  
- 🔴 (Upcoming) Live Chat tab for livestreams.  

---

## 🔧 Installation
### For Chromium Browsers (Chrome, Edge, Brave)  
1. Download or clone this repository.  
2. Open `chrome://extensions/` → Enable **Developer Mode**.  
3. Click **Load unpacked** → Select the `edge-chrome` folder.  

### For Firefox  
1. Open `about:debugging#/runtime/this-firefox`.  
2. Click **Load Temporary Add-on…**.  
3. Select any file inside the `firefox` folder.  

---

## 📂 Project Structure
```bash
yt-sidetabs/
│
├── edge-chrome/   # Manifest V3 (Chromium browsers)
├── firefox/       # Manifest V2 (Firefox stable)
├── assets/        # Screenshots & demo GIF
└── README.md
