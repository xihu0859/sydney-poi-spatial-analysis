# Data sources and dictionary

## Sources and attribution

| Dataset | Provider and source | Use in this project |
| --- | --- | --- |
| NSW regional summary | Australian Bureau of Statistics, [Data by Region: NSW](https://dbr.abs.gov.au/region.html?lyr=ste&rgn=1) | Supplied 800-row source CSV; cleaning and five derived indicators for 2019–2024 |
| SA2 boundaries, ASGS Edition 3 (2021), GDA94 | Australian Bureau of Statistics, [ASGS digital boundary files](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files) | Original national shapefile subset to 128 SA2 polygons; EPSG:4283 retained |
| NSW Points of Interest | NSW Spatial Services, [service metadata](https://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_POI/MapServer) and [dataset catalogue](https://data.nsw.gov.au/data/dataset/nsw-points-of-interest-poi) | Historical bounding-box API extraction, deduplication, exact spatial assignment and aggregation |
| SA2 population eligibility audit | ABS Data by Region, [population feature service](https://services-ap1.arcgis.com/ypkPEy1AmwPKGNNv/arcgis/rest/services/SA2_pop_ppl_DbR_Nov24/FeatureServer/0) | Separate later 123-SA2 audit; not used in the published 128-SA2 score |

Based on Australian Bureau of Statistics data. © Commonwealth of Australia (Australian Bureau of Statistics). ABS website material is generally available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), subject to the exceptions on the [ABS copyright page](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer), including third-party content. The regional summary can include indicators sourced from other agencies; those source rights remain applicable.

© State of New South Wales (Spatial Services, a business unit of the Department of Customer Service NSW). For current information go to [spatial.nsw.gov.au](https://www.spatial.nsw.gov.au/). The POI catalogue resource lists [CC BY 3.0](https://data.nsw.gov.au/data/dataset/nsw-points-of-interest-poi/resource/df67de48-89c4-4941-b20e-7f31a2e53430); the general [Spatial Services copyright page](https://www.spatial.nsw.gov.au/copyright) states CC BY 4.0 unless otherwise stated. Retain the dataset-specific attribution and licence notice when reusing the snapshot. The REST service also displays the legacy notice “© Department of Finance, Services & Innovation 2018”.

Transformations made by the project include selecting study polygons, bounding-box extraction, deduplication by object ID, date conversion, point-in-polygon assignment, regional aggregation and derived statistics. No government endorsement is implied. Sources and notices were checked during repository curation on 31 October 2026. The exact original POI collection timestamp was not recorded; current API content may differ.

## Published scoring table

`results/tables/well_resourced_score_by_sa2.csv` has 128 records, one per SA2.

| Field | Meaning |
| --- | --- |
| `sa4_code21`, `sa4_name21` | 2021 parent SA4 identifier and name |
| `sa2_code21`, `sa2_name21` | 2021 SA2 identifier and name; SA2 code is the row key |
| `area_sqkm` | ABS polygon area in km² from `AREASQKM21` |
| `poi_count` | Unique POIs strictly within the polygon after spatial assignment |
| `poi_density_per_sqkm` | POI count / polygon area |
| `z_score` | Density standardised across all 128 study SA2s using `ddof=0` |
| `well_resourced_score` | `1 / (1 + exp(-z_score))` |
| `rank` | Descending density-score rank |

SA2/SA4 codes are identifiers, not quantities. Missing values in source and derived CSVs remain empty; do not interpret an empty field as zero.

## Included snapshots

- `data/raw/nsw_region_summary.csv`: original supplied NSW CSV, 800 measures with year columns.
- `data/raw/poi_raw_selected_sa4.csv`: 18,209 query records. A POI may appear in multiple overlapping boxes. Bounding-box SA2/SA4 fields describe query provenance, not exact polygon membership.
- `data/raw/selected_sa2_boundaries.geojson`: full-detail geometry of the 128 study polygons, extracted from the submitted map, with only original uppercase boundary attributes retained. This is a subset of the national dataset, not all Greater Sydney.
- `data/interim/poi_cleaned_selected_sa4.csv`: 10,627 deduplicated points with converted timestamps and a WKT geometry column. Some points remain outside the study polygons until spatial assignment.
- `data/interim/cleaned_region_summary_2019_2024.csv`: 279 measures with at least four observed years out of six. Candidate features for derived statistics use a stricter missingness threshold.
- `data/audit/`: the later population-filter audit, with 123 eligible and five excluded SA2s. Its counts must not be mixed with the published score cohort.
- `results/tables/poi_count_by_sa2_database.csv` and `poi_count_by_sa4_database.csv`: exact spatial aggregation. The SA4 total is 9,042.
- `results/tables/well_resourced_score_sql_check.csv`: saved SQL implementation output, independently reconciled against the Python scores.
- `results/tables/derived_yearly_statistics_2019_2024.csv`: six year rows and five derived NSW indicators. The first unnamed CSV column contains the year index.
- `results/maps/`: original result GeoJSON (EPSG:4283) and Folium HTML (web-map coordinates). These are historical outputs.

The redundant `cleaned_data_1.csv` scratch table, a duplicate NSW source CSV and national shapefile are omitted. No coordinates from personal tracking or private address data were introduced; the POI coordinates originate from the cited public government service.
