-- Requires tables loaded by notebooks/sydney_poi_analysis.ipynb
WITH poi_counts AS (
    SELECT
        s."SA4_CODE21" AS sa4_code21,
        s."SA4_NAME21" AS sa4_name21,
        s."SA2_CODE21" AS sa2_code21,
        s."SA2_NAME21" AS sa2_name21,
        s."AREASQKM21" AS area_sqkm,
        COUNT(p.*) AS poi_count
    FROM sydney_poi_portfolio.sa2_regions s
    LEFT JOIN sydney_poi_portfolio.poi p
        ON s."SA2_CODE21" = p.sa2_code21
    WHERE s."SA4_CODE21" IN (125,119,117,121)
    GROUP BY
        s."SA4_CODE21",
        s."SA4_NAME21",
        s."SA2_CODE21",
        s."SA2_NAME21",
        s."AREASQKM21"
),
density AS (
    SELECT
        *,
        poi_count::DOUBLE PRECISION / NULLIF(area_sqkm, 0) AS poi_density_per_sqkm
    FROM poi_counts
),
scored AS (
    SELECT
        *,
        (
            poi_density_per_sqkm - AVG(poi_density_per_sqkm) OVER ()
        ) / NULLIF(STDDEV_POP(poi_density_per_sqkm) OVER (), 0) AS z_score
    FROM density
)
SELECT
    DENSE_RANK() OVER (ORDER BY 1 / (1 + EXP(-z_score)) DESC) AS rank,
    sa4_code21,
    sa4_name21,
    sa2_code21,
    sa2_name21,
    poi_count,
    area_sqkm,
    poi_density_per_sqkm,
    z_score,
    1 / (1 + EXP(-z_score)) AS well_resourced_score
FROM scored
ORDER BY rank;
