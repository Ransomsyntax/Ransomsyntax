# RansomSyntax — Unified Platform

This is the merged Django project combining:

- **Main website** (`ransomsyntax_website`) — served at `/`
- **Education platform** ("RANSOM SYNTAX — Learn Your Skills", formerly `ransom-syntax-edu` / `suryamaxcode`) — served at `/students/`

Both now run as one Django project, one settings file, one database, and
one set of static/media files. Neither site's design, templates,
animations, layout, or branding was changed. The only visible change is
that the main site's existing **"For Students"** navbar button now links
to the education platform instead of scrolling to the `#courses` section.

---

## Project structure

```
project/
├── manage.py
├── config/                  # project settings, root urls, wsgi/asgi
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── website/                 # main marketing site (unchanged)
├── core/                    # education platform: home/about pages
├── accounts/                # education platform: auth, custom User, dashboards
├── courses/                 # education platform: courses, videos, enrollment
├── chatbot/                 # education platform: help-widget chatbot
├── templates/
│   ├── website/              # main site templates (unchanged)
│   ├── admin/                 # custom admin dashboard template
│   ├── base.html               # education platform base template
│   ├── core/, accounts/, courses/   # education platform templates (unchanged)
├── static/
│   ├── css/, img/, js/        # main site static assets (unchanged, original paths)
│   └── edu/                    # education platform static assets
│       ├── css/, img/, js/     # (moved here only to avoid filename collisions
│                                  with the main site's own css/img/js folders —
│                                  content is untouched, only the {% static %}
│                                  paths referencing them were updated)
├── media/
│   ├── teachers/, videos/     # education platform uploads
├── requirements.txt
├── .env.example
└── .gitignore
```

Four Django apps power the education platform (`core`, `accounts`,
`courses`, `chatbot`) instead of one, mirroring the original project's own
app structure — nothing was collapsed or renamed, so each app's existing
namespace (`core:`, `accounts:`, `courses:`, `chatbot:`) still works
exactly as it did before the merge.

---

## URL map

### Main website (unchanged)
| URL | View |
|---|---|
| `/` | Home (single-page site) |
| `/privacy-policy/` | Privacy policy |
| `/terms-conditions/` | Terms & conditions |
| `/api/chat/` | Chat widget endpoint |
| `/sitemap.xml`, `/robots.txt` | SEO |

### Education platform (new `/students/` prefix)
| URL | View |
|---|---|
| `/students/` | Student home |
| `/students/about/` | About |
| `/students/login/` | Student login |
| `/students/register/` | Student registration |
| `/students/teacher/login/` | Teacher login |
| `/students/logout/` | Logout |
| `/students/dashboard/` | Student dashboard |
| `/students/dashboard/edit-profile/` | Edit profile |
| `/students/profile/` | Alias for the edit-profile page above |
| `/students/teacher/dashboard/` | Teacher dashboard |
| `/students/courses/` | Course list |
| `/students/courses/<slug>/` | Course detail |
| `/students/courses/enquiry/` | Course enquiry form |
| `/students/courses/teacher/...` | Teacher video/course management |
| `/students/chatbot/ask/` | Help-widget chatbot endpoint |

All of these URLs resolve through each app's own `app_name` namespace
(`core`, `accounts`, `courses`, `chatbot`), so every `{% url %}` tag inside
the education platform's templates needed **zero changes** — only the
outer prefix moved from the site root to `/students/`.

---

## What changed vs. what didn't

**Did not change:**
- Any HTML/CSS/JS content, layout, colors, or animations on either site.
- Any view logic, forms, or model field on either site.
- The main website's static file paths (`static/css/...`, `static/img/...`, `static/js/...`) — identical to before.
- Any of the education platform's URL names or `app_name` namespaces.

**Did change (structural/plumbing only):**
- Project folder layout: `ransomsyntax/` → `config/`, both apps now live
  side by side in one project instead of two separate `manage.py` roots.
- The education platform's static assets moved into `static/edu/` (both
  projects had a `static/css/style.css`, `static/img/logo.png`, etc. with
  *different* content — namespacing was required to avoid one silently
  overwriting the other). The corresponding `{% static %}` tags in the
  education platform's templates were updated to match.
- `AUTH_USER_MODEL = "accounts.User"` is now set project-wide. This is
  safe: the main website's models (`Service`, `Course`, `ClientEnquiry`)
  have no relationship to the user model at all.
- One line in `templates/website/includes/navbar.html`: the existing
  "For Students" button's `href` now points to the education platform's
  home page instead of `#courses`.
- Settings, URLs, requirements, and admin branding were merged (see below).

---

## Settings merge notes

- **Django version**: pinned to `Django>=5.0,<5.3` (the main site's
  requirement). The education platform was built against Django 4.2 but
  uses no version-specific APIs, so it runs unchanged on Django 5.x.
- **Context processor**: both projects had a nearly identical
  `site_settings` / `site_info` context processor exposing `SITE_NAME`,
  `SITE_TAGLINE`, `SITE_YOUTUBE_URL`, `SITE_INSTAGRAM_URL` (the main
  site's version also adds `SITE_CONTACT_EMAIL`). Only the main site's
  version (`website.context_processors.site_settings`) is registered —
  it's a strict superset, so every variable either template used is still
  available.
- **TIME_ZONE**: kept as `Asia/Kolkata` (the education platform's
  setting), since that's the platform's actual operating region.
- **Admin branding**: both projects set `admin.site.site_header` etc.
  `website` is listed last in `INSTALLED_APPS` so its richer admin
  dashboard (with enquiry/service/course stats on the index page) is the
  one that ends up active — this preserves "main website stays primary."
- **MEDIA / STATIC**: single shared `MEDIA_ROOT` / `STATIC_ROOT` for both
  sites; `whitenoise` continues to serve static files in production.

---

## Setup instructions

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# edit .env and set a real DJANGO_SECRET_KEY, at minimum

# 4. Run migrations
python manage.py migrate

# 5. Create an admin (superuser) account
python manage.py createsuperuser

# 6. (Optional) seed demo education-platform data
python manage.py seed_demo

# 7. Collect static files (only needed for production / whitenoise)
python manage.py collectstatic --noinput

# 8. Run the dev server
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/` — main website
- `http://127.0.0.1:8000/students/` — education platform (via the "For Students" navbar button)
- `http://127.0.0.1:8000/admin/` — Django admin

### ⚠️ Verification note
This merge was assembled and carefully reviewed line-by-line (every
`{% url %}`, `{% static %}`, URL pattern, model relationship, and admin
registration was traced by hand for collisions), but it has **not yet
been run against a live Django install** in the environment this was
produced in (no network/package access there). Please run
`python manage.py check`, then `migrate`, then `runserver` as your first
real smoke test, and let me know if anything surfaces — most likely
candidates for a first-run hiccup would be a missing `Pillow` system
dependency (for `ImageField`) or a stray `__pycache__`/migration cache
artifact, both easy fixes.

---

## Production deployment

- Set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY` in `.env`.
- Set `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` to your real domain(s).
- Run `python manage.py collectstatic` before deploying — `whitenoise` serves the result.
- Use `gunicorn config.wsgi:application` behind a reverse proxy (nginx, etc.).
- Make sure `media/` is on persistent storage (or move to S3/equivalent) — course videos and profile photos are stored there.
#   R a n s o m s y n t a x  
 