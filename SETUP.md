# Tickets: setup

Two GitHub repos:

| Repo | Visibility | Holds |
|---|---|---|
| `tickets` | **private** | `tickets.json`, `tickets.py`, `claude-skill/SKILL.md` (your data, from `C:\Users\dlarouche\tickets`) |
| `tickets-app` | public | `index.html`, `manifest.webmanifest`, `icon.svg` (the app, no data) |

The app repo is public only because GitHub Pages is free for public repos. It holds no tickets; each device keeps its own token.

## 1. GitHub (once)

1. Sign in at github.com, or create an account.
2. Create a **private** repo named `tickets`, empty (no README).
3. Create a **public** repo named `tickets-app`, empty.
4. Create a token: Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token.
   - Repository access: **Only select repositories** → `tickets`.
   - Permissions → Repository → **Contents: Read and write**.
   - Pick an expiry (up to a year; you'll paste a new one in the app when it runs out).
   - Copy the token (`github_pat_…`).

## 2. Push the data (this PC)

Claude can run these for you once you give it your GitHub username:

```bash
cd ~/tickets
git init -b main
git config user.name "YOUR NAME"
git config user.email "YOUR_GITHUB_EMAIL"
git add -A && git commit -m "Initial tickets"
git remote add origin https://github.com/YOUR_USERNAME/tickets.git
git push -u origin main
```

Git asks you to sign in to GitHub in the browser the first time.

## 3. Publish the app

Upload the three app files (`index.html`, `manifest.webmanifest`, `icon.svg`) to `tickets-app`, either through **Add file → Upload files** on GitHub or with git. Then go to Settings → Pages → Source: **Deploy from a branch**, `main`, `/ (root)` → Save.

After a minute it's at `https://YOUR_USERNAME.github.io/tickets-app/`.

## 4. Each device

**Browser (any PC):** open the app URL, then ⚙ → enter your username, `tickets`, and the token → **Save & connect**.

**Phone:** open the URL, connect the same way, then add it to your home screen. On iPhone: Safari → Share → **Add to Home Screen**. On Android: Chrome → ⋮ → **Add to Home screen**.

**Claude on the personal PC:**

```bash
git clone https://github.com/YOUR_USERNAME/tickets.git ~/tickets
mkdir -p ~/.claude/skills/todo && cp ~/tickets/claude-skill/SKILL.md ~/.claude/skills/todo/
```

Then set `git config user.name` / `user.email` inside `~/tickets`, like on this PC.

## Notes

- Using a personal GitHub account from a work PC may be covered by your company's IT policy; check if unsure.
- The app saves instantly, shows **Synced** / **Saving…** in the corner, and refreshes when you come back to it or every 30 s. If two devices change things at the same time, both changes are kept.
- The token stays in that browser's storage. **Sign out** in ⚙ removes it from the device. If a phone is lost, delete the token on GitHub.
- To test the app without GitHub: `python mock_github.py ~/tickets/tickets.json`, open http://localhost:8766, and in ⚙ → Advanced set the API URL to `http://localhost:8766`.
