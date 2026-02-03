# 🌌 Wormhole File Transfer

**Stop messaging yourself. Just toss it!**

Fast & Hassle-free Wormhole makes it easy to transfer files yourself. This application is powered by the Telegram API.

![image](docs/pictures/running.gif)

---

## 1. Overview
* **Drag & Drop Transfer:** Drag any file onto the wormhole widget to send it instantly to your Telegram.
* **Auto Environment:** As long as Python is installed, double-clicking `run.bat` (Windows) or `run.sh` (Linux/macOS) will automatically handle everything from virtual environment setup to execution.
* **Customizing:** Use the settings panel to freely adjust the widget's opacity and default rotation speed.

---

## 2. Installation & Execution

> **Note:** This is a GUI-based widget and cannot be used in a terminal-only (headless) environment.

### 1) Python Installation
This program was developed in `python=3.11`. \
Although other versions of python were supported, I recommend this version considering dependencies.

* **Download Python 3.11.14:** ```https://www.python.org/downloads/```
* **Note:** When you installing, please check **"Add Python to PATH"** !

### 2) Creating a Telegram Bot
You need to set up a bot to act as your personal transfer channel.
1. Search for **@BotFather** on Telegram and start a chat.

![image](docs/pictures/find_botfather.gif)

2. Use the `/newbot` command to create a bot and receive your **Bot Token**.

![image](docs/pictures/make_newbot.gif)

3. Start your new bot.

![image](docs/pictures/start_newbot.gif)

4. Copy & paste your **Bot Token** at this URL. \
Then, open the URL at the browser, and chat any words to your bot. \
Finally, you can get **Chat ID** when refreshing the browser.

> `https://api.telegram.org/bot[BOT TOKEN]/getUpdates`

![image](docs/pictures/get_chat_id.png)

5. Memorize your **Bot Token**, **Chat ID** !

### 3) Running the App by OS

* **Windows 🪟**
  - Double-click the `run.bat` file in the project folder.
* **Linux / macOS 🍎🐧**
  - Open a terminal and run `./run.sh`.
  - (If a permission error occurs, run `chmod +x run.sh` first.)

---

## 3. How to use?

### 1) Input your Bot Token & Chat ID
* Wait a second... you can see the Wormhole is opening. Go to **Settings(설정)** menu at the system tray.
* Register your **Bot Token** and **Chat ID**, and then **Save(저장)** .

![image](docs/pictures/setup_wormhole.png)

### 2) Sending Files and Text
* Drag and drop files or images onto the **purple wormhole widget** on your screen.
* The wormhole accelerates during transfer, and a system tray notification will appear once the transfer is complete.

![image](docs/pictures/running.gif)

### 3) Checking Messages and Clipboard
* **Double-click the edge of the wormhole widget.**
* Your Telegram bot chat will open immediately, allowing you to check sent history or copy text.

![image](docs\pictures\open_browser.gif)

---

## 4. Settings

### 1) Configuration
* **Bot Token / Chat ID:** Modify your Telegram integration info.
* **Opacity:** Adjust the widget's transparency so it doesn't interfere with your work.
* **Rotation Speed:** Set the default rotation speed of the wormhole to your preference.

### 2) System Tray
* Right-click the taskbar icon to access the following features:
  - **Show/Hide Wormhole:** Temporarily hide or reveal the widget.
  - **Settings:** Open the configuration dialog.
  - **Quit:** Exit the program completely.

---

## 5. Copyrights
* This project is licensed under the **MIT License**.
* Anyone is free to modify and redistribute this software.

## 6. Credits
- `src/assets/andromeda.jpg`

![image](src/assets/andromeda.jpg) \
Captured by **NASA/JPL-Caltech/Univ. of Ariz. (Spitzer Space Telescope)** \
(https://images.nasa.gov/details/PIA07828)