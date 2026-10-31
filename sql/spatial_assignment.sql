-- Requires tables loaded by notebooks/sydney_poi_analysis.ipynb
UPDATE sydney_poi_portfolio.poi p
SET sa2_code21 = s."SA2_CODE21"
FROM sydney_poi_portfolio.sa2_regions s
WHERE ST_Within(p.geometry, s.geometry)
  AND s."SA4_CODE21" IN (125,119,117,121);
