# 🏙️ North American City Bigness Index

> *"The underlying purpose of this is to determine which cities **feel** the biggest — not necessarily which ones are biggest by population."*

A data-driven ranking of 60 US and Canadian metro areas by **functional urban scale** — how large a city feels based on its skyline, infrastructure, sports presence, landmarks, and economic gravity, not just its headcount.

---

## 🧠 The Idea

Population rankings don't tell the whole story. Chicago feels larger than Los Angeles despite having fewer people. Las Vegas punches far above its metro size. Phoenix disappoints relative to its population. This project quantifies *why*.

Inspired by manually ranking cities in Excel — cross-referencing skyline density, airport traffic, sports teams, and landmarks to produce a composite "bigness" score.

---

## 📊 Metrics

### Phase 1 — Original 4-Metric Model
| Metric | Source |
|--------|--------|
| Metro Population Rank | US Census / Statistics Canada |
| Skyline Score | CTBUH Skyscraper Center (topped-out buildings counted) |
| Airport Throughput | FAA / Transport Canada (consolidated metro airports) |
| Sports Teams | NFL, NBA, MLB, NHL weighted by tier |

### Phase 2 — Expanded 8-Metric Model
Adds four additional metrics to Phase 1:

| Metric | Notes |
|--------|-------|
| Transit Ridership | Heavy rail / metro annual riders |
| Convention Center Capacity | Largest venue sq ft in metro |
| Corporate HQs | Fortune 500 / TSX equivalent |
| Landmark Score | Tiered: world-famous (10pts), national (5pts), regional (2pts) |

---

## 🏆 Methodology

Two scoring methods are run and compared side by side:

- **Rank Aggregation** — average of individual metric ranks (lower = better). Simple, transparent, matches the original Excel model
- **Z-Score Normalization** — standardizes raw values before compositing, reducing distortion from extreme outliers

Phase 1 rank aggregation replicates the original handmade Excel ranking with **51/55 exact matches** — the 4 divergences are tiebreaker differences only.

---

## 🗂️ Project Structure

```
cityscapes/
├── build_db_v2.py            # Builds the SQLite database from source data
├── city_bigness_v2.db        # Generated SQLite database (7 tables, 60 cities)
└── city_bigness_index.ipynb  # Full analysis + charts
```

### Database Schema
```
cities               → master list + metro pop rank + notes
skyline_data         → cumulative height-band counts + skyline rank
airports             → passengers, airport count, IATA codes, rank
sports_teams         → NFL/NBA/MLB/NHL counts + sports rank
transit_systems      → system name + annual riders
convention_centers   → venue name + sq ft
landmarks            → tiered landmark list (natural + manmade)
corporate_hq         → Fortune 500 / TSX equivalent HQ count
```

---

## 🚀 How to Run

**Requirements:**
```
pip install pandas matplotlib seaborn jupyter
```

**Steps:**
```bash
# 1. Build the database
python build_db_v2.py

# 2. Launch Jupyter
jupyter notebook

# 3. Open city_bigness_index.ipynb and run Kernel → Restart & Run All
```

Charts will save as PNG files to your working directory.

---

## 📐 Skyline Scoring Notes

Skyline data uses **cumulative height bands** matching CTBUH conventions:

| Band | Description |
|------|-------------|
| 100m+ | Low-rise density baseline |
| 150m+ | Solid skyline contributors |
| 200m+ | Major skyscrapers |
| 250m+ | Significant towers |
| 300m+ | Supertalls |

**Key decisions:**
- Topped-out buildings are counted (structural height is real)
- Miami includes the full South Florida corridor (Sunny Isles, Fort Lauderdale, Hollywood)
- Washington DC is credited with the Northern Virginia skyline (Rosslyn, Tysons, Crystal City) due to the Height Act
- Toronto includes two topped-out 300m+ towers (SkyTower at Pinnacle One Yonge + The One)

---

## 🗺️ Cities Included

60 metro areas across the US and Canada, ranging from New York City (#1) to Mobile, Alabama and Quebec City at the tail. Includes major Canadian metros: Toronto, Montreal, Vancouver, Calgary, Edmonton, Ottawa, Winnipeg, Quebec City.

---

## 📌 Notable Results

- **Chicago #2** — ranks Top 5 in every single category
- **Las Vegas +14** — biggest riser when expanded metrics are added (Strip + Grand Canyon proximity + world's largest convention center)
- **Washington DC** — penalized heavily in Phase 1 due to the Height Act; recovers significantly in Phase 2 via landmarks and transit
- **Phoenix** — most disappointing skyline relative to metro size (#53 skyline despite #13 population)
- **Calgary** — most noticeable discrepancy between city size and cityscape (#44 population, #13 skyline)
- **Orlando** — airport and convention center carry it far above what its skyline or sports presence would suggest

---

## 🔧 Updating the Data

To update when notable buildings top out or teams relocate:

1. Edit the relevant city entry in `build_db_v2.py`
2. Re-run `python build_db_v2.py`
3. Re-run the notebook

Or open `city_bigness_v2.db` directly in [DB Browser for SQLite](https://sqlitebrowser.org/) for visual editing.

---

## 📝 License

MIT — use freely, attribution appreciated.
