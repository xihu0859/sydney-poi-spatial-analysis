"""Rebuild the historical point-in-polygon counts independently using Shapely 2."""
from collections import Counter
from pathlib import Path
import csv
import json
from shapely.geometry import Point, shape
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[1]


def verify_spatial():
    geo = json.loads((ROOT / 'data/raw/selected_sa2_boundaries.geojson').read_text(encoding='utf-8'))
    features = geo['features']
    tree = STRtree([shape(f['geometry']) for f in features])
    counts = Counter()
    seen = set()
    raw_count = 0
    assigned = 0
    with (ROOT / 'data/raw/poi_raw_selected_sa4.csv').open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            raw_count += 1
            if not row['lon'] or not row['lat'] or row['objectid'] in seen:
                continue
            seen.add(row['objectid'])
            point = Point(float(row['lon']), float(row['lat']))
            matches = tree.query(point, predicate='within')
            assert len(matches) <= 1, 'Ambiguous overlapping SA2 polygons'
            if len(matches):
                code = str(features[int(matches[0])]['properties']['SA2_CODE21'])
                counts[code] += 1
                assigned += 1
    with (ROOT / 'results/tables/poi_count_by_sa2_database.csv').open(encoding='utf-8-sig', newline='') as stream:
        expected = {r['sa2_code21']: int(r['poi_count']) for r in csv.DictReader(stream)}
    actual = {str(f['properties']['SA2_CODE21']): counts[str(f['properties']['SA2_CODE21'])] for f in features}
    assert actual == expected, 'Spatial counts differ from the historical PostGIS export'
    assert (raw_count, len(seen), assigned) == (18209, 10627, 9042)
    return {'raw_rows': raw_count, 'unique_valid_pois': len(seen), 'assigned_pois': assigned, 'sa2_counts_matched': len(expected)}


if __name__ == '__main__':
    print(json.dumps(verify_spatial(), indent=2))
