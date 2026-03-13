# PyCharm: Push to GitHub — Step-by-Step Setup

## Prerequisites

- Project is already a Git repository (e.g. you ran `git init` in the project root).
- You have a GitHub account and a repository created (e.g. `https://github.com/YOUR_USERNAME/t23b.org`).
- For push, GitHub requires a **Personal Access Token (PAT)**, not your account password.

---

## Step 1: Enable Git in PyCharm

1. Open **PyCharm** and open your project folder (`t23b.org`).
2. Go to **File → Settings** (on macOS: **PyCharm → Preferences**).
3. Open **Version Control → Git**.
4. In **Path to Git executable**, ensure the path is correct (PyCharm usually finds it).
5. Click **OK**.

---

## Step 2: Add GitHub as a Remote (if not added yet)

1. Menu **Git → Manage Remotes...** (or **VCS → Git → Remotes...** in some versions).
2. Click **+** (Add).
3. **Name:** `origin`
4. **URL:** `https://github.com/YOUR_USERNAME/t23b.org.git`  
   Replace `YOUR_USERNAME` with your GitHub username.
5. Click **OK**, then **OK** again.

---

## Step 3: Log In to GitHub from PyCharm (first time)

1. Go to **File → Settings** (or **PyCharm → Preferences**).
2. Open **Version Control → GitHub** (or **Tools → GitHub** in older versions).
3. Click **Add Account...**.
4. Choose **Log in via GitHub** (opens browser) or **Log in with Token**.
   - **With Token (recommended):**  
     - Create a token: GitHub → **Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token**.  
     - Give it a name, select scope **repo**, generate and copy the token.  
     - In PyCharm, paste the token as the password (username = your GitHub username).
5. Click **OK**. Your account should appear in the list.
6. Click **OK** to close Settings.

---

## Step 4: Commit Changes (before each push)

1. Open the **Commit** tool window: **View → Tool Windows → Commit** (or **Alt+6** / **Ctrl+6**).
2. In the left panel you’ll see changed files. Select the files you want to commit (or leave all selected).
3. Enter **Commit Message** (e.g. `Add footer checks` or `Fix TC-04 date logic`).
4. Click **Commit** (or **Commit and Push** if you want to push right away).
   - To only commit: choose **Commit** (not “Commit and Push”).

---

## Step 5: Push to GitHub

1. Menu **Git → Push...** (or **Ctrl+Shift+K** / **Cmd+Shift+K**).
2. In the **Push** dialog you’ll see:
   - **Commit(s)** to push (e.g. 1 commit on `main`).
   - **Remote:** `origin`, **Branch:** `main`.
3. Click **Push**.
4. If PyCharm asks for credentials:
   - **Username:** your GitHub username.
   - **Password:** your **Personal Access Token** (not your GitHub account password).
5. After a successful push, the dialog closes and the code is on GitHub.

---

## Optional: Push with one action after commit

- In the **Commit** window, use **Commit and Push** instead of **Commit**.  
- Or after committing: **Git → Push...** (or **Ctrl+Shift+K** / **Cmd+Shift+K**).

---

## Summary checklist

| Step | Action |
|------|--------|
| 1 | **Settings → Version Control → Git** — check Git path. |
| 2 | **Git → Manage Remotes** — add `origin` with your repo URL. |
| 3 | **Settings → Version Control → GitHub** — add GitHub account (token). |
| 4 | **Commit** tool window — select files, message, **Commit** (or **Commit and Push**). |
| 5 | **Git → Push** — push to `origin` / `main`. |

After this, your usual flow is: change code → **Commit** (with message) → **Push**.
