# Youtube Comments, Description, Related, Playlist Right/Side Panel  

![Status](https://img.shields.io/badge/status-active-success)  
![Firefox](https://img.shields.io/badge/firefox-supported-orange?logo=firefox) 
![Chrome](https://img.shields.io/badge/chrome-supported-green?logo=google-chrome) 
![Edge](https://img.shields.io/badge/edge-supported-blue?logo=microsoft-edge)  
![License](https://img.shields.io/badge/license-MIT-blue)  
![MadeWith](https://img.shields.io/badge/made%20with-JavaScript-yellow?logo=javascript)  

> A lightweight browser extension that adds a **right-hand sidebar with tabs** for YouTube.  
> Instantly switch between **Comments, Description, Related Videos, and Playlist** without endless scrolling.  

<p align="center">
  <img src="assets/demo.gif" alt="Extension Demo" width="720px">
</p>  

---

## Features
- Tabbed right sidebar → **Comments, Description, Related, Playlist** (auto-detected).  
- Seamlessly blends with YouTube (light & dark mode).  
- No page reloads, no external requests, no tracking.  
- Playlist detection → adds playlist tab only when available.  
- Planned: Live Chat support for YouTube livestreams.  

---

## Installation
### For Chromium Browsers (Chrome, Edge, Brave)  
1. Download or clone this repository.  
2. Open `chrome://extensions/` → Enable **Developer Mode**.  
3. Click **Load unpacked** → Select the `edge-chrome` folder.  

### For Firefox  
1. Open `about:debugging#/runtime/this-firefox`.  
2. Click **Load Temporary Add-on…**.  
3. Select any file inside the `firefox` folder.  

---

## Project Structure
```bash
yt-sidetabs/
│
├── edge-chrome/   # Manifest V3 (Chromium browsers)
├── firefox/       # Manifest V2 (Firefox stable)
├── assets/        # Screenshots & demo GIF
└── README.md
