from flask import Flask, render_template, abort, send_from_directory
from pathlib import Path
import markdown
import time
import re

app = Flask(__name__)

POSTS_DIR     = Path(__file__).parent / 'posts'
PORTFOLIO_DIR = Path(__file__).parent / 'data' / 'portfolio'
APPS_DIR      = Path(__file__).parent / 'data' / 'apps'
CACHE_TTL     = 3600  # seconds

_posts_cache:     list  = []
_portfolio_cache: list  = []
_apps_cache:      list  = []
_posts_at:        float = 0
_portfolio_at:    float = 0
_apps_at:         float = 0

TAG_COLORS    = {'code': 'blue', 'design': 'pink', 'art': 'yellow', 'games': 'green', 'music': 'teal', 'prints': 'peach'}
TAG_LABELS    = {'code': 'CODE', 'design': 'DESIGN', 'art': 'ART', 'games': 'GAME', 'music': 'MUSIC', 'prints': '3D PRINT'}
STATUS_COLORS = {'live': 'green', 'beta': 'yellow', 'in progress': 'overlay1'}


# ── Shared frontmatter parser ──────────────────────────────────────────────────

def _parse_fm(text):
    meta, body = {}, text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) == 3:
            for line in parts[1].strip().splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"')
            body = parts[2].strip()
    return meta, body


def _slug_from_stem(stem):
    return re.sub(r'^\d+-', '', stem)


# ── Blog posts ─────────────────────────────────────────────────────────────────

def parse_post(slug):
    path = POSTS_DIR / f'{slug}.md'
    if not path.exists():
        return None
    meta, body = _parse_fm(path.read_text(encoding='utf-8'))
    meta['slug'] = slug
    meta['html'] = markdown.markdown(body, extensions=['fenced_code', 'tables'])
    return meta


def _load_posts():
    posts = []
    for path in sorted(POSTS_DIR.glob('*.md'), reverse=True):
        post = parse_post(path.stem)
        if post and post.get('draft') != 'true':
            posts.append(post)
    return posts


def get_all_posts():
    global _posts_cache, _posts_at
    if time.time() - _posts_at > CACHE_TTL:
        _posts_cache = _load_posts()
        _posts_at = time.time()
    return _posts_cache


# ── Portfolio ──────────────────────────────────────────────────────────────────

def _load_portfolio():
    items = []
    for path in sorted(PORTFOLIO_DIR.glob('*.md')):
        meta, body = _parse_fm(path.read_text(encoding='utf-8'))
        cat = meta.get('category', 'code')
        meta['tag_color'] = TAG_COLORS.get(cat, 'text')
        meta['tag_label'] = TAG_LABELS.get(cat, cat.upper())
        meta['slug'] = _slug_from_stem(path.stem)
        meta['html'] = markdown.markdown(body, extensions=['fenced_code', 'tables']) if body else ''
        items.append(meta)
    return items


def get_portfolio():
    global _portfolio_cache, _portfolio_at
    if time.time() - _portfolio_at > CACHE_TTL:
        _portfolio_cache = _load_portfolio()
        _portfolio_at = time.time()
    return _portfolio_cache


def get_portfolio_item(slug):
    return next((i for i in get_portfolio() if i['slug'] == slug), None)


# ── Apps ───────────────────────────────────────────────────────────────────────

def _load_apps():
    apps = []
    for path in sorted(APPS_DIR.glob('*.md')):
        meta, body = _parse_fm(path.read_text(encoding='utf-8'))
        meta['status_color'] = STATUS_COLORS.get(meta.get('status', ''), 'overlay0')
        meta['slug'] = _slug_from_stem(path.stem)
        meta['html'] = markdown.markdown(body, extensions=['fenced_code', 'tables']) if body else ''
        apps.append(meta)
    return apps


def get_apps():
    global _apps_cache, _apps_at
    if time.time() - _apps_at > CACHE_TTL:
        _apps_cache = _load_apps()
        _apps_at = time.time()
    return _apps_cache


def get_app_item(slug):
    return next((a for a in get_apps() if a['slug'] == slug), None)


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    posts = get_all_posts()
    featured_portfolio = [i for i in get_portfolio() if i.get('featured') == 'true']
    featured_apps = [a for a in get_apps() if a.get('featured') == 'true']
    return render_template('index.html', current='home',
                           latest_post=posts[0] if posts else None,
                           featured_portfolio=featured_portfolio,
                           featured_apps=featured_apps)


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', current='portfolio', items=get_portfolio())


@app.route('/portfolio/<slug>')
def portfolio_item(slug):
    item = get_portfolio_item(slug)
    if not item:
        abort(404)
    return render_template('portfolio-item.html', current='portfolio', item=item)


@app.route('/apps')
def apps():
    return render_template('apps.html', current='apps', apps=get_apps())


@app.route('/apps/<slug>')
def app_item(slug):
    item = get_app_item(slug)
    if not item:
        abort(404)
    return render_template('app-item.html', current='apps', item=item)


@app.route('/blog')
def blog():
    return render_template('blog.html', current='blog', posts=get_all_posts())


@app.route('/blog/<slug>')
def blog_post(slug):
    post = parse_post(slug)
    if not post:
        abort(404)
    return render_template('blog-post.html', current='blog', post=post)


@app.route('/uses')
def uses():
    return render_template('uses.html', current='uses')


@app.route('/tools/botc-token-labels')
def botc_tool():
    return send_from_directory('static/tools', 'botc-token-labels.html')
