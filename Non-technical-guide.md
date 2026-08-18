# Notes Maker — The Friendly, No-Jargon Setup Guide

This guide is for people who are **comfortable using a computer but are not programmers**.
If you can install an app, copy and paste, and follow steps in order, you can set this up.
Take it slowly — you only have to do the setup **once**.

**What does this tool do?** You give it a web article, a YouTube video, or some text you
paste in. It reads the content, writes a clean, tidy summary for you, and saves it as a
note. Over time you build up a neat, searchable collection of notes.

We'll go through everything: the programs you need, a free "AI key", an optional online
backup for your notes, installing the tool, and using it day to day.

---

## Before you start: a few words you'll see

- **Terminal** (also called *Command Prompt*, *PowerShell*, or *Command Line*): a plain
  window where you type commands instead of clicking buttons. Don't worry — you'll just be
  copying and pasting.
- **Command**: a line of text you paste into the terminal and then press **Enter** to run.
- **API key**: a long secret password that lets this tool talk to Google's AI. It's free to
  get. Keep it private, like a real password.
- **Repository (repo)**: just a fancy word for a **folder** that holds your notes.

### How to open a terminal

- **Windows**: Press the **Start** button, type `PowerShell`, and click **Windows
  PowerShell**.
- **Mac**: Press **Cmd + Space**, type `Terminal`, and press **Enter**.
- **Linux**: Open your **Terminal** app from the applications menu.

You'll paste commands into this window throughout the guide. To paste: **Ctrl + V** on
Windows/Linux, **Cmd + V** on Mac (in some terminals you right-click to paste).

---

## Step 1 — Install two small helper programs

This tool needs two free programs to work: **uv** (which installs and runs Notes Maker) and
**Git** (which can back your notes up online). Install both once and forget about them.

### 1a. Install `uv`

`uv` is a small, free tool that installs Notes Maker for you.

- **Windows**: Open PowerShell and paste this, then press Enter:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Mac or Linux**: Open your terminal and paste this, then press Enter:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

When it finishes, **close the terminal window and open a new one** so the change takes
effect. To check it worked, type `uv --version` and press Enter — you should see a version
number. (If you see "command not found", restart your computer and try again.)

### 1b. Install `Git`

Git is what lets Notes Maker save a backup of your notes online (Step 3). It's optional, but
recommended.

- **Windows**: Download and run the installer from <https://git-scm.com/download/win>. Click
  **Next** through the installer — the default choices are fine.
- **Mac**: In the terminal type `git --version` and press Enter. If Git isn't installed, your
  Mac will offer to install it — accept.
- **Linux**: Use your package manager, e.g. `sudo apt install git` on Ubuntu.

---

## Step 2 — Get your free AI key (Gemini)

Notes Maker uses Google's **Gemini** AI to write your summaries. You need a free key.

1. Go to <https://aistudio.google.com/apikey> in your web browser.
2. Sign in with your normal Google account.
3. Click **Create API key** (follow any prompts — accept the terms if asked).
4. A long string of letters and numbers appears. Click **Copy**.
5. **Paste it somewhere safe for a moment** — like a temporary note. You'll need it in Step
   5. Treat it like a password: don't share it or post it anywhere.

That's it — you now have your AI key.

---

## Step 3 — (Recommended) Set up an online backup for your notes

This step keeps a safe copy of your notes online using **GitHub**, a free website for
storing files. If you skip it, your notes still save on your computer — you just won't have
an online backup. You can always do this later.

1. **Make a free GitHub account** at <https://github.com/join> if you don't have one.
2. **Create a place for your notes**:
   - Click the **+** in the top-right of GitHub and choose **New repository**.
   - Give it a name, for example `my-notes`.
   - Choose **Private** (so only you can see it).
   - Click **Create repository**.
3. On the next page, GitHub shows a web address ending in `.git`. It looks like:
   `https://github.com/yourname/my-notes.git`. **Copy it and keep it for later** — you'll
   use it in Step 6.

You don't need to understand the technical parts — just keep that `.git` address handy.

---

## Step 4 — Install Notes Maker

Open a fresh terminal window and paste this command, then press Enter:

```bash
uv tool install git+https://github.com/Afnan-Ahmad961/notes-maker
```

Wait for it to finish (it may take a minute). When it's done, the command `notes-maker` is
now available anywhere on your computer.

To check it worked, type `notes-maker` and press Enter. It should start asking you questions
— that's Step 5. (If it says "command not found", close the terminal, open a new one, and
try again.)

---

## Step 5 — The first-time setup (answering two questions)

The **very first time** you run `notes-maker`, it asks you two things and remembers your
answers forever after. Run it now if you haven't:

```bash
notes-maker
```

1. **"Paste your Gemini API key"** — Paste the AI key you copied in Step 2 and press Enter.
   (You may not see any characters appear as you paste — that's normal, it's hidden for
   privacy.)
2. **"Notes Repository Path"** — This is the **folder on your computer** where your notes
   will be saved. Type a folder path and press Enter. For example:
   - **Windows**: `C:\Users\YourName\Documents\my-notes`
   - **Mac/Linux**: `~/Documents/my-notes`

   If the folder doesn't exist yet, Notes Maker creates it for you. Your notes always save
   here, no matter where you run the command from.

That's the whole setup. You won't be asked these again.

> **Want to change these later?** They're saved in a small settings file. To start over,
> you can delete that file and you'll be asked again next time. Its location:
> - **Windows**: `%LOCALAPPDATA%\notes-maker\notes-maker\.env`
> - **Mac**: `~/Library/Application Support/notes-maker/.env`
> - **Linux**: `~/.config/notes-maker/.env`

---

## Step 6 — (Only if you did Step 3) Connect your online backup

Do this **once** to link your notes folder to the GitHub place you made in Step 3. Your notes
are saved inside a `notes` sub-folder, and that's the folder we connect. Paste these
commands **one at a time** (press Enter after each). Replace the folder path with the one you
chose in Step 5, and the web address with your own `.git` address from Step 3:

```bash
cd "C:\Users\YourName\Documents\my-notes\notes"
git init
git remote add origin https://github.com/yourname/my-notes.git
```

(On Mac/Linux the first line would be `cd ~/Documents/my-notes/notes`.)

That's all. From now on, Notes Maker will offer to upload your notes for you automatically —
you don't have to remember any of these commands again.

---

## Step 7 — Making notes (your everyday use)

This is the fun part, and it's all clicking and pasting. Run:

```bash
notes-maker
```

Then answer the friendly prompts (use the **arrow keys** to move between choices and
**Enter** to pick one):

1. **How do you want to input the source?**
   - **URL** — for a web article. You'll paste the article's link.
   - **YouTube** — for a video. You'll paste the video's link. (It reads the video's
     subtitles, so the video must have captions available.)
   - **Raw Text** — to paste your own text. Paste it in, then press **Enter twice on an
     empty line** to tell it you're done.
2. **Which file should this summary go into?** — Pick an existing notes file, or choose
   **Create a new file** and give it a simple name like `technology` or `cooking`. This lets
   you keep different topics in different files.
3. **Wait a few seconds** while the AI writes your summary. You'll see it appear.
4. **"Commit and push to Git?"** — If you set up the online backup (Steps 3 and 6), choose
   **Yes** to save a copy online. If you didn't, choose **No** — your note is still saved on
   your computer either way.

Done! Your note is saved, neatly titled and dated, and added to a table of contents at the
top of the file so you can find it easily later.

---

## Keeping Notes Maker up to date

Every now and then, get the latest improvements by pasting this:

```bash
uv tool upgrade notes-maker
```

---

## If something goes wrong

- **"command not found" after installing** — Close the terminal completely, open a new one,
  and try again. If it still happens, restart your computer.
- **It asks for your API key again** — Your saved key may be empty or wrong. Get a fresh key
  from <https://aistudio.google.com/apikey> and paste it when asked.
- **An AI error about your key or quota** — Free keys have daily limits. Wait a while and try
  again, or check your key at the Google link above.
- **A YouTube video won't work** — The video probably has no captions/subtitles. Try a
  different video, or use the **Raw Text** option with a transcript you have.
- **The online backup (push) didn't work** — Make sure you finished Step 6 and that your
  internet is connected. Your notes are still safe on your computer; you can try the upload
  again next time.

---

## Quick recap

1. Install **uv** and **Git** (Step 1).
2. Get a free **Gemini AI key** (Step 2).
3. *(Optional)* Make a **GitHub** account and notes repository for online backup (Step 3).
4. Install the tool: `uv tool install git+https://github.com/Afnan-Ahmad961/notes-maker`
   (Step 4).
5. Run `notes-maker` once and answer the two setup questions (Step 5).
6. *(Optional)* Connect the online backup one time (Step 6).
7. Run `notes-maker` whenever you want to make a note (Step 7).

Enjoy your tidy, automatic notes!
