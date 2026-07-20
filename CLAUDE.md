# Portfolio — Ondřej Řepka

## Stack
Flask (Python) + Jinja2 templates + vanilla CSS/JS. No build step.

## Running locally
```bash
source venv/bin/activate
flask --app app run
```

## Structure
```
app.py                  — Flask routes, parsers, 1-hour cache for all data
requirements.txt        — Flask, Markdown, gunicorn
posts/                  — Blog posts (.md files)
data/
  portfolio/            — Portfolio items (.md files, numbered for order)
  apps/                 — Apps & Tools (.md files, numbered for order)
templates/
  base.html             — Shared navbar, head, script tag
  index.html            — Home page (pulls featured portfolio + apps from data)
  portfolio.html        — Portfolio grid with category filter
  portfolio-item.html   — Single portfolio item page
  apps.html             — Apps & Tools grid
  blog.html             — Blog post list
  blog-post.html        — Single blog post
  uses.html             — Hardware & software list (hardcoded)
static/
  style.css             — Catppuccin CSS variables + all component styles
  main.js               — Theme toggle, portfolio filter
  uploads/              — Images for posts/portfolio
  tools/                — Self-contained tool HTML files
    botc-token-labels.html
Caddyfile               — Caddy reverse proxy config (ondrej.repka.org → :5001)
portfolio.service       — systemd service file for Gunicorn
WRITING.md              — Guide for adding content (posts, portfolio, apps)
```

## Content — see WRITING.md for full guide

**Blog post** → `posts/2026-07-25-slug.md`
**Portfolio item** → `data/portfolio/NN-slug.md`
**App/Tool** → `data/apps/NN-slug.md`

Filename number prefix controls display order. Cache refreshes every hour; restart service to force immediate update.

## Portfolio categories
`code` · `design` · `art` · `games` · `music` · `prints`

Add `featured: true` to a portfolio item or app to show it on the home page.

## Design system
- **Theme**: Catppuccin Mocha (dark) / Latte (light) — toggled via `data-theme` on `<html>`, persisted in `localStorage` key `ondrej-theme`
- **Fonts**: Space Grotesk (headings) · Inter (body) · JetBrains Mono (labels/code)
- **Colors**: CSS custom properties (`--p-mauve`, `--p-base`, etc.) — palette colour helper classes in style.css (`c-blue`, `bg-red`, etc.) avoid Jinja2 inside inline styles

## Adding a hosted tool
1. Drop the self-contained HTML file in `static/tools/`
2. Add a route in `app.py`: `send_from_directory('static/tools', 'filename.html')`
3. Add an entry in `data/apps/` with `url:` pointing to the route

## Deployment
Site runs at `ondrej.repizz.org` on homelab server `repka` (Ubuntu) via Caddy (Docker) + Gunicorn + systemd.

### Server: repka (user: repizz)
- Gunicorn binds to `0.0.0.0:5001` (must be 0.0.0.0, not 127.0.0.1, so Docker Caddy can reach it)
- Caddy runs in Docker with `network_mode: host` — compose file at `/home/repizz/docker/caddy/`
- UFW allows ports 80, 443 (Caddy) and 5001 from `172.17.0.0/16` (Docker bridge)
- Caddyfile at `/home/repizz/docker/caddy/Caddyfile` — uses `localhost:5001` as upstream

### Deploy flow (after pushing to GitHub)
```bash
# On repka
cd ~/portfolio
git pull
sudo systemctl restart portfolio
```

### First-time setup on a new server
```bash
cd ~/portfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo cp portfolio.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now portfolio

sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow from 172.17.0.0/16 to any port 5001
```

### Caddy (Docker) — reload config
```bash
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

Caddy handles TLS automatically via Let's Encrypt.

## Source
Original design: `Portfolio blog and apps site.zip` (Claude Design export, kept for reference).
