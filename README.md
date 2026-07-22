# PINE Workflows

Internal showcase for digital tools and agents built by the PINE team. A single-page directory where each department can preview its live apps and track upcoming projects.

## Overview

**PINE workflows** is a static internal portal — not a multi-app monorepo. It links out to department tools hosted elsewhere and embeds live previews where available.

| Item | Detail |
|------|--------|
| **Purpose** | Internal solution directory for 9 departments |
| **Stack** | Static HTML, CSS, vanilla JavaScript |
| **Hosting** | [Vercel](https://vercel.com) |
| **Repo** | [Eldar0904/pine-solutions](https://github.com/Eldar0904/pine-solutions) |

## Project structure

```
pine-solutions/
├── pine-solutions.html   # Entire app (HTML + CSS + JS)
├── vercel.json           # Rewrites / → pine-solutions.html
└── README.md
```

There are no build steps, frameworks, or npm dependencies.

## How it works

### Department tabs

Use the filter bar (**Выберите направление**) to switch views:

| Tab | View |
|-----|------|
| **Оперблок** | Live preview of OperBlock |
| **Гос. закуп** | Live preview of Goszakup database |
| **Юр отдел** | Live preview of ЮрОтдел |
| **Академический**, **B2B**, **PR**, **Финансы**, **Дистрибуция**, **Склад** | Placeholder previews (coming soon) |
| **Скорo** | Pipeline cards for projects in development or planning |

### Live department apps

These tabs embed the app in an iframe and provide an **Открыть** link that opens the full app in a new tab:

| Department | App | URL |
|------------|-----|-----|
| Оперблок | OperBlock | https://operblock-production.up.railway.app/ |
| Гос. закуп | База данных Госзакупок | https://pinegroup-gz.onrender.com/ |
| Юр отдел | ЮрОтдел — создание договоров | https://quick-dogovor.netlify.app/ |

### Скоро (coming soon)

The **Скорo** tab shows compact cards for upcoming work:

1. **Оперблок** — ИИ Агент — мобильный ассистент *(Разработка)*
2. **B2B** — ИИ поиск поставщиков *(Планирование)*
3. **Финансы** — Программа для финансиста *(Планирование)*

Each card has a status dropdown: Работает · Разработка · Тестирование · Планирование.

### Workflow CTA

The **«Предложить workflow»** section at the bottom is a placeholder for future intake (e.g. OperBlock form or external link). It is not wired yet.

## Local development

Open the file directly in a browser:

```bash
# From the repo root — any static server works
npx serve .
# or
python -m http.server 8080
```

Then visit `http://localhost:8080/pine-solutions.html` (or `/` if using a server that respects `vercel.json` rewrites).

## Deployment

Deployed on **Vercel** from the `main` branch. `vercel.json` rewrites the root path to `pine-solutions.html`:

```json
{
  "rewrites": [
    { "source": "/", "destination": "/pine-solutions.html" }
  ]
}
```

Push to `main` to trigger a redeploy:

```bash
git add .
git commit -m "Your message"
git push origin main
```

## Editing content

Most text on the page is **contenteditable** — click any label, title, or description in the browser to edit inline. A short hint appears on first load.

To add or change a live department preview permanently, edit `pine-solutions.html`:

1. Find the `.dept-preview-card` with the matching `data-dept` code (`ops`, `proc`, `legal`, etc.).
2. Update the title, **Открыть** `href`, browser URL bar text, and iframe `src`.
3. For placeholder departments, keep `href="#"` — clicks are blocked automatically.

### Department codes

| Code | Department |
|------|------------|
| `ops` | Оперблок |
| `proc` | Гос. закуп |
| `legal` | Юр отдел |
| `acad` | Академический |
| `b2b` | B2B |
| `pr` | PR |
| `fin` | Финансы |
| `dist` | Дистрибуция |
| `wh` | Склад |
| `soon` | Скорo (coming-soon grid) |

## Related apps (external)

These run on their own infrastructure and are linked from this showcase:

- **OperBlock** — Railway + Neon Postgres + Clerk auth
- **Goszakup** — Render (+ Supabase sync)
- **ЮрОтдел** — Netlify (+ Supabase)

## License

Internal use — PINE team · 2026
