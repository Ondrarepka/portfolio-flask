# Content writing guide

## Creating a post

1. Create a file in `posts/` — the filename becomes the URL slug.
   - Name it with a date prefix so posts sort newest-first:
     `posts/2026-07-25-my-post-title.md`
   - URL will be: `yourdomain.com/blog/2026-07-25-my-post-title`

2. Start every file with frontmatter (the `---` block):

```
---
title: My post title
date: Jul 2026
tag: dev
excerpt: One sentence shown on the blog index and home page.
---
```

3. Write your content below the second `---` in normal Markdown.

That's it. Refresh the site and the post appears.

---

## Frontmatter fields

| Field     | Required | Notes                                              |
|-----------|----------|----------------------------------------------------|
| `title`   | yes      | Displayed as the big H1 on the post page           |
| `date`    | yes      | Shown on the index (e.g. `Jul 2026`)               |
| `tag`     | yes      | Label in pink (e.g. `dev`, `meta`, `life`, `tools`)|
| `excerpt` | yes      | Short summary — keep it one sentence               |
| `draft`   | no       | Set to `true` to hide the post from the index      |

---

## Links

```markdown
[Link text](https://example.com)

[Link to another post](/blog/2026-07-20-some-other-post)
```

Internal links (to pages on your own site) start with `/`:

```markdown
[Check my portfolio](/portfolio)
[Back to blog](/blog)
```

---

## Images

1. Put the image file in `static/uploads/`
2. Reference it in your post:

```markdown
![Description of the image](/static/uploads/your-image.png)
```

Example with a caption below (just normal text after):

```markdown
![Screenshot of the terminal](/static/uploads/habit-tracker.png)
*The finished terminal UI — dark mode only, obviously.*
```

The `/static/uploads/` path is what Flask serves — it must start with `/static/` to work correctly.

---

## Text formatting

```markdown
**bold**
*italic*
~~strikethrough~~
`inline code`
```

## Headings

```markdown
## Section heading
### Sub-section
```

(Don't use `#` H1 — the post title is already rendered as H1 by the template.)

## Lists

```markdown
- Item one
- Item two
  - Nested item

1. First
2. Second
3. Third
```

## Code blocks

Fenced with triple backticks and an optional language for syntax highlighting:

````markdown
```python
def hello():
    print("hello world")
```

```bash
flask --app app run
```
````

## Blockquotes

```markdown
> This is a quote.
> It can span multiple lines.
```

## Horizontal rule (section divider)

```markdown
---
```

---

## Drafts

Add `draft: true` to frontmatter to keep a post hidden while you're working on it:

```
---
title: Work in progress
date: Jul 2026
tag: dev
excerpt: Not ready yet.
draft: true
---
```

It won't appear on the blog index or home page. Remove the line (or set it to `false`) when you're ready to publish.

---

---

## Adding a portfolio item

Create a file in `data/portfolio/`. Prefix the filename with a number to control the display order:

```
data/portfolio/09-my-new-project.md
```

Frontmatter fields:

| Field         | Required | Notes                                                      |
|---------------|----------|------------------------------------------------------------|
| `title`       | yes      | Displayed on the card                                      |
| `category`    | yes      | `code`, `design`, `art`, `games`, or `music` — drives the filter buttons |
| `blurb`       | yes      | One or two sentences shown under the title                 |
| `placeholder` | yes      | Text shown in the striped placeholder when no image is set              |
| `image`       | no       | Path to an image — shown instead of the placeholder if set             |
| `featured`    | no       | Set to `true` to show this item in the Featured work section on the home page |

Example:

```
---
title: My New Project
category: code
blurb: A tool that does something clever and probably involves cats.
placeholder: screenshot of the thing
---
```

To add an image, drop it in `static/uploads/` and set the `image` field:

```
image: /static/uploads/my-project.png
```

The image fills the thumbnail at 16:10 on cards and 21:9 on the item page — it's cropped to fit, so landscape photos work best. Without `image`, the striped placeholder with your `placeholder` text is shown instead.

---

## Adding an app or tool

Create a file in `data/apps/`. Same numbering convention for order:

```
data/apps/06-my-new-tool.md
```

Frontmatter fields:

| Field         | Required | Notes                                                                 |
|---------------|----------|-----------------------------------------------------------------------|
| `name`        | yes      | Displayed as the card title                                           |
| `initials`    | yes      | 2–3 characters shown in the icon                                      |
| `color`       | yes      | Palette key for the icon background: `mauve`, `red`, `peach`, `teal`, `overlay0` |
| `status`      | yes      | `live`, `beta`, or `in progress`                                      |
| `description` | yes      | One or two sentences                                                  |
| `url`         | no       | Link for the "Try it" button — use `/tools/name` for hosted tools     |
| `repo`        | no       | Link for the "Source" button                                          |
| `new_tab`     | no       | Set to `true` to open `url` in a new tab                             |
| `featured`    | no       | Set to `true` to show this item in the Apps & Tools section on the home page |

Example:

```
---
name: My Tool
initials: MT
color: mauve
status: live
description: Does one thing and does it well.
url: /tools/my-tool
new_tab: true
---
```

If neither `url` nor `repo` is set, no buttons appear on the card.

Each app card links to its own page at `/apps/slug`. Add a body below the frontmatter to write a description, backstory, or technical notes — same Markdown as blog posts.

---

## Deploying updates to the server

After pushing changes to GitHub, SSH into the server and run:

```bash
cd ~/portfolio
git pull
sudo systemctl restart portfolio
```

The site at `ondrej.repizz.org` will reflect the changes immediately.

---

## Quick example post

```markdown
---
title: The keyboard that ate my productivity
date: Jul 2026
tag: tools
excerpt: A review of the loudest mechanical keyboard I've ever owned.
---

Six months ago I bought a keyboard that sounds like a small appliance.
My neighbours know when I'm working. My cat leaves the room.

## The good

It feels *incredible* to type on. Every keystroke is an event.

## The bad

[This video](https://example.com) is a fair representation of the noise level.

Here's what my desk looks like now:

![My desk setup](/static/uploads/desk.jpg)

Would I recommend it? Absolutely. Would I recommend it to someone who shares
an office? **No.**
```
