# Provenance and reproduction

## What was preserved

The submitted Group31 folder is the source for the report, notebook, map files and CSV exports. Published tables and maps retain their original numerical values. The original source directory was left unchanged.

The report is a layout-cleaned copy: one repeated methodology page and a blank final page were removed. Remaining page content was retained. Document metadata was replaced with a neutral project title and Group31 authorship. Its discussion should be read with the qualifications in `findings.md`.

The notebook was curated for portability. Paths resolve from the repository, credentials come from an environment variable, generated runs go to `results/reproduced/`, and the default reads the historical POI snapshot. A compact boundary file contains the 128 ABS study polygons without score fields. Saved notebook outputs were cleared because the source had mixed execution states.

## The 128/123-SA2 discrepancy

The final folder's notebook includes a later population-filter edit. It identifies five regions below 100 residents and retains 123 SA2s. However, downstream API logs, count tables, score exports, GeoJSON and the report still describe 128 SA2s and 9,042 assigned POIs. The score export has no population column. These artifacts do not demonstrate an end-to-end run of the later filter.

This repository uses the **128-region published report cohort**. The unpropagated population-filter section and population-dependent database fields have been removed from the main notebook to match the results. The 123-region eligibility CSV and exclusion audit remain separately in `data/audit/`; they are not inputs to the published scores. The excluded audit's geometry reflects the original ABS polygons and its population field comes from the later ABS service lookup. Exact population reference year was not recorded reliably by the source's field-selection fallback, so it is not asserted here.

Applying that filter is a new analysis: recalculate spatial assignments, cohort mean and standard deviation, scores, tables and maps together. Removing five rows from an existing ranked table does not reproduce a filtered-cohort score.

## Quick independent checks

```bash
python scripts/verify_results.py
python -m pip install "shapely>=2,<3"
python scripts/verify_spatial_join.py
```

The first command independently recalculates density, population-standard-deviation z-scores, sigmoid values and rankings from published counts and areas. It compares the saved Python/SQL exports, top and bottom tables, SA4 totals and map properties. It also recalculates the five derived indicators directly from the raw ABS CSV.

The second script uses Shapely's `within` predicate and STRtree, independently of PostGIS, on the raw query snapshot and selected boundaries. It deduplicates object IDs, assigns points and compares every SA2 count with the saved database export. Both checks passed locally during curation: 18,209 raw rows, 10,627 unique valid POIs, 9,042 assigned POIs and 128 matching regional counts.

The scripts validate the supplied snapshot, not completeness of the original API extraction, live API availability, or the present state of a PostgreSQL database. The GitHub Actions workflow is supplied but has not been run remotely before upload.

## Full analysis notebook

Use Python 3.11 or newer in a virtual environment. Install the notebook dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Activate the environment first, or invoke its Python executable explicitly when installing. Install PostgreSQL with the PostGIS extension separately. Create a dedicated empty database named `sydney_poi`, owned by a role that can enable PostGIS and create schemas.

Set environment variables before starting Jupyter. PowerShell example:

```powershell
$env:DATABASE_URL = 'postgresql+psycopg2://USER:PASSWORD@localhost:5432/sydney_poi'
$env:ANALYSIS_SCHEMA = 'sydney_poi_portfolio'
python -m jupyter lab
```

Replace the example values with your own credentials and URL-encode special characters in a password. `.env.example` is a configuration guide; the notebook does not automatically load `.env`. Do not commit credentials.

Open `notebooks/sydney_poi_analysis.ipynb` and run in order. The database section refuses an existing schema, so use a fresh schema name for each run. It creates project tables and indexes, assigns POIs using `ST_Within`, stores scores and implements the same calculation in SQL using window functions and `STDDEV_POP`. SQL rank uses `DENSE_RANK` to agree with Pandas for tied values. Full PostgreSQL execution was not rerun during curation; Python cell syntax and the independent snapshot checks were verified.

Generated files go to `results/reproduced/`, which is ignored by Git. Compare them with the committed tables before replacing any published artifacts.

## Live collection

`REFRESH_POIS = False` uses the saved snapshot. Setting it to `True` makes a new extraction through the original bounding-box loop. API error responses and `exceededTransferLimit` now fail explicitly, rather than silently accepting an incomplete result. Pagination must be implemented before using a query that hits the service limit. The population endpoint from the unpropagated edit is not used by the report-cohort notebook.

The saved collection date was not recorded in the original data. It is a historical coursework snapshot, not a current inventory. Requerying an evolving service can change identifiers, counts and rankings.

## Git history

The local repository uses one `main` branch and current, task-based commits for imported results, reproducibility code and documentation. These commits describe the curation work; they do not represent the original team's development chronology. There are no fabricated past commits or contribution claims.
