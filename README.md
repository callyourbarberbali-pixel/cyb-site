# CYB — Mobile Barbershop site

A single-page site with a free, no-code content dashboard.

**The free stack:**
- **GitHub** — stores the site files + uploaded photos
- **Sveltia CMS** — the dashboard at `/admin` where you edit text and upload photos (no coding)
- **Netlify** — hosts the live site for free

You log in to the dashboard with a GitHub **Personal Access Token** — so there's **no OAuth app or Cloudflare Worker to set up.**

---

## Files in this folder
- `index.html` — the website
- `content.json` — all editable text/photos (the dashboard writes to this)
- `admin/index.html` + `admin/config.yml` — the dashboard
- `images/uploads/` — where uploaded photos land

---

## STEP-BY-STEP

### Part 1 — Put the site on GitHub
1. Make a free account at **github.com**.
2. Click **New repository**. Name it `cyb-site`, set it **Public**, click **Create repository**.
3. On the repo page: **Add file → Upload files**. Drag in **everything** from this folder
   (`index.html`, `content.json`, the `admin` folder, the `images` folder). Click **Commit changes**.
4. Open `admin/config.yml` on GitHub → click the **pencil** (Edit) → change this line:
   ```
   repo: YOUR_GITHUB_USERNAME/cyb-site
   ```
   to your real username and repo name (e.g. `repo: madebudi/cyb-site`). Commit.

### Part 2 — Put it live on Netlify
5. Go to **netlify.com** → **Sign up** (choose "Sign up with GitHub" — easiest).
6. **Add new site → Import an existing project → GitHub →** pick `cyb-site`.
7. Leave build settings empty (Build command: blank, Publish directory: blank / root). Click **Deploy**.
8. In ~30 seconds you get a live URL like `random-name.netlify.app`. (Rename it under **Site settings → Change site name**, or add a custom domain later.)

### Part 3 — Log into the dashboard
9. Go to **your-site-url/admin/** (the trailing slash matters).
10. Click **Sign in with Token**. It opens GitHub with the right permissions pre-selected →
    **Generate token** → copy it → paste it back into the dashboard. (One-time. Pick a long expiry.)
11. You're in. Open **Site Content** and edit:
    - WhatsApp number + Instagram handle  ← **do this first or the Book buttons won't work**
    - Services & prices
    - Service areas
    - Barber bio
    - **Gallery** — click **＋**, upload a photo, give it a label
12. Click **Save → Publish**. It commits to GitHub, Netlify rebuilds, and the live site updates in ~30 sec.

---

## Tips
- **Compress phone photos first** (free: squoosh.app) — raw 5 MB photos make the site slow. Aim for under ~400 KB each.
- To edit later, just go back to `/admin/`. No code, ever.
- The site still works if `content.json` fails to load — it falls back to built-in defaults.
- Want the nicer one-click "Login with GitHub" instead of a token? That needs a free Cloudflare Worker
  (Sveltia's `sveltia-cms-auth`). Optional — the token method is fine for one person.
