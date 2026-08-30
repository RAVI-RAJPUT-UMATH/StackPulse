# StackPulse

An interactive dashboard for exploring how programming language popularity has shifted over time, based on Stack Overflow tag activity. Pick any set of languages and compare their long-term trends, month-by-month usage, and share of the conversation in a single month.

A Flask API serves the data and also hosts the frontend, so the whole thing runs from one command and one port.

---

## Features

- **Compare any languages** — select from 30 tracked tags; charts update together with a consistent colour per language.
- **Three linked views**
  - *Trends Over Time* — line chart of each language's share across every month.
  - *Monthly Popularity* — grouped bar chart for month-to-month movement.
  - *Distribution by Month* — doughnut showing the split for a single month, with percentages drawn on the slices and in the legend.
- **Section routing** — the sidebar opens each chart as a full-page view (`#trends`, `#monthly`, `#distribution`) with working back/forward navigation and shareable URLs.
- **Selection-aware doughnut** — with languages selected it shows only those, re-based so they total 100%; with nothing selected it falls back to all 30.
- **Quick controls** — Top 5 shortcut, Clear, and a live search filter over the language list.
- **Live summary cards** — language count, months tracked, most popular tag with its month-over-month change, and how many languages are currently selected.
- **Dark / light theme** — follows the OS by default, with a toggle that persists in `localStorage`.
- **Responsive** — desktop grid down to an off-canvas drawer on mobile; charts resize and their legends and axis tick density adapt per breakpoint.

---

## Tech stack

| Layer    | Built with                                  |
| -------- | ------------------------------------------- |
| Backend  | Flask, Flask-CORS, pandas                   |
| Frontend | Vanilla HTML/CSS/JS, Chart.js 4 (CDN)       |
| Data     | `computed_data.csv` — a precomputed monthly table |

No build step and no `node_modules` — the frontend is a single self-contained `index.html`.

---

## Project structure

```
StackPulse/
├── backend/
│   ├── app.py               # Flask API + static host for the frontend
│   ├── computed_data.csv    # 37 months x 30 languages
│   └── requirements.txt
├── frontend/
│   └── index.html           # Entire UI: markup, styles, and charts
└── README.md
```

---

## Getting started

**Requirements:** Python 3.8+

```bash
git clone https://github.com/RAVI-RAJPUT-UMATH/StackPulse.git
cd StackPulse

# optional but recommended
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r backend/requirements.txt

cd backend
python app.py
```

Open **http://127.0.0.1:5000** — Flask serves the dashboard and the API from the same origin.

> Opening `frontend/index.html` directly from the filesystem also works: it detects the `file://` protocol and falls back to `http://127.0.0.1:5000` for API calls, which CORS allows. The backend still needs to be running.

---

## API

| Method | Endpoint                        | Returns |
| ------ | ------------------------------- | ------- |
| `GET`  | `/`                             | The dashboard (`frontend/index.html`) |
| `GET`  | `/api/data`                     | Every language's full monthly series |
| `GET`  | `/api/pie_data?month=YYYY-MM`   | One month's distribution across all languages |

`/pie_data` is kept as an alias of `/api/pie_data`. The `month` parameter is optional and defaults to the most recent month in the dataset.

**`GET /api/data`**

```json
{
  "year_month": ["2022-04", "2022-05", "..."],
  "python":     [17.15, 16.90, "..."],
  "javascript": [11.76, 11.92, "..."]
}
```

**`GET /api/pie_data?month=2025-04`**

```json
{
  "labels": ["android", "angular", "..."],
  "values": [3.57, 3.57, "..."]
}
```

Errors come back as `{"error": "..."}`. `/api/pie_data` returns `400` for an unknown month and `500` if the CSV is missing or unreadable; `/api/data` reports the same problems in the body with a `200` status.

---

## Data

`backend/computed_data.csv` holds **37 months** (2022-04 → 2025-04) across **30 languages**. The first column is `year_month`; every other column is a tag whose value is that tag's percentage share of Stack Overflow question activity for the month.

```csv
year_month,android,angular,arrays,...,typescript
2022-04,3.672316384180791,1.6692347200821775,...,2.2598870056497176
```

To use your own data, replace the CSV keeping that shape — the backend reads the column names at runtime, so the frontend picks up new languages automatically with no code changes.

---

## Notes

- Charts update when **Compare Selected** is pressed, not on every checkbox tick, so all three stay in sync with one selection.
- The doughnut fetches a month once and re-filters it locally when the selection changes, avoiding a request per toggle.
- Chart colours are drawn from a fixed palette by selection order, so a language keeps the same colour across all three charts.

---

## Author

**Ravi Rajput** — [rr-developer.netlify.app](https://rr-developer.netlify.app/)
