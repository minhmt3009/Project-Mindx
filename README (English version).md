# Spotify Analytics Studio – Music Data Analysis Dashboard

A Spotify data analysis capstone project featuring an interactive dashboard to explore, search, filter, and analyze comprehensive track metrics (genre, artist, country, label, stream counts, popularity, etc.), powered by a Python web server (backend).


## 1. Project overview

The project consists of two core components:

  1. Data Processing (Python Backend): Reads a Spotify track dataset (.csv format hosted on GitHub), performs computations, and filters/sorts records across various criteria.
  2. User Interface (Dashboard – dashboard.html): Renders processed metrics into charts, world maps, and data tables for clear, intuitive visualization.


## 2. Key Feature

Dashboard được chia thành nhiều khu vực chức năng:

  - The dashboard is structured into several functional modules:
  - Overview: High-level metrics for an immediate summary of the dataset.
  - Search: Query tracks by unique track ID or song title.
  - Multi-Criteria Filtering: Combine filters across genre, artist, release year, record label, country, and loudness simultaneously.
  - Track Management: Add new tracks (with auto-generated track IDs) or delete existing entries.
  - Rankings & Statistics:
    + Top tracks by highest and lowest stream counts.
    + Top tracks by popularity score.
    + Total streams ranked by genre.
    + Total streams grouped by release year.
  - Average popularity per genre, segmented into High / Moderate / Low Popularity.
  - Release volume distributed by calendar quarter.
  - In-Depth Record Label Analysis: Track count, total streams, and signed artist counts per label to evaluate market influence.
  - Geographic Analysis: Country-level track volume and total streams mapped onto an interactive global projection.



## 3. Project structure

| File | Role |
|---|---|
| `main.py` | Central Coordinator: Boots the web server, handles dashboard requests, and delegates tasks to the corresponding processing modules. |
| `data_processing.py` | Handles search and multi-attribute filtering (genre, artist, year, label, country, loudness, ID, title). |
| `data_handle.py` | Manages CRUD operations (add/delete tracks) and calculates core rankings/aggregations (streams, popularity, quarterly releases, country statistics). |
| `data_ultilize.py` | Computes specialized record label analytics (track counts, cumulative streams, roster size). |
| `dashboard.html` | The frontend interface containing all visualizations, tables, and map displays. |



## 4. Input data

The project processes a Spotify track dataset stored as a CSV file (`spotify_data_processed.csv`). Key fields include: track ID, track name, artist, genre, country, record label, release date, loudness, popularity score, and stream count.

> **Dynamic Pathing Feature:** The codebase is fully configured with **automatic dynamic path resolution** (`BASE_DIR = os.path.dirname(os.path.abspath(__file__))`). Data files are automatically discovered within the project folder. You can clone or copy this repository to any environment (Drive C, D, macOS, or Linux) and run it immediately **without modifying file paths manually**. All track additions/deletions automatically synchronize back to this file.



## 5. Requirements

Required runtime environment:
- **Python 3.8+**
- Python libraries: `pandas`, `flask`, `flask-cors`, `flask-compress`

Install dependencies using:

```bash
pip install pandas flask flask-cors flask-compress
```



## 6. How to run

1. Ensure `spotify_data_processed.csv` is located in the same directory as `main.py` (automatically detected).
2. Open a terminal in the project root directory (or launch in your IDE).
3. Start the server:

   ```bash
   python main.py
   ```
4. Once initialized, access the dashboard in your web browser:

   ```
   http://localhost:8888
   ```

5. Explore the interactive dashboard: search, multi-filter, examine record label dossiers, view the world heatmap, and manage tracks.

6. **Publishing the Server (Optional):** To share the dashboard externally, tunnel the local port using tools like ngrok:
   
   ```bash
   ngrok http 8888
   ```

   
## 7. API reference

These are the backend API endpoints consumed by the interactive dashboard:

| Endpoint | Description |
|---|---|
| `/api/all` | Retrieves paginated records from the full dataset. |
| `/api/summary` | Retrieves a condensed track summary list. |
| `/api/filter` | Multi-parameter filtering (genre, artist, year, label, country, loudness). |
| `/api/search` | Queries tracks by track ID or title. |
| `/api/suggest` | Provides track name auto-suggestions (autocomplete). |
| `/api/new` | Adds a new track record. |
| `/api/remove` | Deletes a track record by ID or song title. |
| `/api/streamcount` | Returns highest- and lowest-streamed tracks. |
| `/api/popular` | Returns the most popular tracks. |
| `/api/genrecountcrank` | Ranks total stream volume by music genre. |
| `/api/yearcountrank` | Returns aggregate stream counts by release year. |
| `/api/poprank` | Calculates average genre popularity with tiered classifications. |
| `/api/quarterrank` | Aggregates track release frequency by fiscal quarter. |
| `/api/label1`, `/api/label2`, `/api/label3` | Detailed label metrics: track volume, total streams, and artist count. |
| `/api/labeldetails` | **In-depth Label Dossier:** KPIs, top artists roster, genre breakdown, hit songs, markets, and release trends. |
| `/api/countrystats` | Compiles track and stream volume aggregated by country (powers the World Heatmap). |
| `/api/countrydetails` | **In-depth Country Analytics:** Market overview, top artists, albums, genres, and historical trends. |



## 8. Limitation and roadmap

- **Dynamic Pathing (Completed):** Fully migrated to dynamic relative paths (`BASE_DIR` + `CSV_FILE`), guaranteeing cross-platform portability.
- **Data Persistence:** Current write operations commit directly to the local CSV; future upgrades can integrate SQLite or PostgreSQL for enhanced concurrency and data integrity.
- **Expanded Intelligence:** Future iterations can incorporate Content-Based Music Recommendation and deeper acoustic correlations (Energy, Danceability, Valence).

