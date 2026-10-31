"""Independently verify the published snapshot. Python standard library only."""
from pathlib import Path
import csv
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check_close(actual, expected, label):
    if not math.isclose(float(actual), float(expected), rel_tol=1e-9, abs_tol=1e-10):
        raise AssertionError(f"{label}: {actual} != {expected}")


def verify():
    tables = ROOT / "results/tables"
    score = rows(tables / "well_resourced_score_by_sa2.csv")
    sql = rows(tables / "well_resourced_score_sql_check.csv")
    assert len(score) == 128 and len({r['sa2_code21'] for r in score}) == 128
    assert sum(int(r['poi_count']) for r in score) == 9042
    densities = [int(r['poi_count']) / float(r['area_sqkm']) for r in score]
    mean, std = statistics.mean(densities), statistics.pstdev(densities)
    sql_by_code = {r['sa2_code21']: r for r in sql}
    assert set(sql_by_code) == {r['sa2_code21'] for r in score}
    scores = []
    for r, density in zip(score, densities):
        z = (density - mean) / std
        value = 1 / (1 + math.exp(-z))
        scores.append(value)
        for key, expected in [('poi_density_per_sqkm', density), ('z_score', z), ('well_resourced_score', value)]:
            check_close(r[key], expected, f"{r['sa2_code21']} {key}")
            check_close(sql_by_code[r['sa2_code21']][key], expected, f"SQL export {r['sa2_code21']} {key}")
    assert scores == sorted(scores, reverse=True)
    ranks = {value: i + 1 for i, value in enumerate(sorted(set(scores), reverse=True))}
    for r, value in zip(score, scores):
        assert int(r['rank']) == ranks[value]
        assert int(sql_by_code[r['sa2_code21']]['rank']) == ranks[value]
    for name, expected in [('top_10_well_resourced_sa2.csv', score[:10]), ('bottom_10_well_resourced_sa2.csv', score[-10:])]:
        actual = rows(tables / name)
        assert [r['sa2_name21'] for r in actual] == [r['sa2_name21'] for r in expected]
    sa4_counts = {}
    for r in score:
        key = r['sa4_code21']
        sa4_counts[key] = sa4_counts.get(key, 0) + int(r['poi_count'])
    assert sa4_counts == {r['sa4_code21']: int(r['poi_count']) for r in rows(tables / 'poi_count_by_sa4_database.csv')}
    geo = json.loads((ROOT / 'results/maps/well_resourced_score_map.geojson').read_text(encoding='utf-8'))
    assert len(geo['features']) == 128
    by_code = {r['sa2_code21']: r for r in score}
    for feature in geo['features']:
        p = feature['properties']
        r = by_code[str(p['SA2_CODE21'])]
        check_close(p['well_resourced_score'], r['well_resourced_score'], 'map score')
        assert int(p['poi_count']) == int(r['poi_count'])

    # Recalculate all five state-level statistics from the original ABS source rows.
    raw = rows(ROOT / 'data/raw/nsw_region_summary.csv')
    by_measure = {r['Measure Code'].strip(): r for r in raw}
    published = rows(tables / 'derived_yearly_statistics_2019_2024.csv')
    def number(code, year):
        text = by_measure[code][str(year)].replace(',', '').strip()
        try:
            return float(text)
        except ValueError:
            return math.nan
    for r in published:
        year = int(r[''])
        pop = number('ERP_P_20', year)
        previous = number('ERP_P_20', year - 1) if year > 2019 else math.nan
        expected = {
            'population_growth_rate_percent': (pop / previous - 1) * 100,
            'female_to_male_ratio': number('ERP_F_20', year) / number('ERP_M_20', year),
            'natural_increase': number('BD_2', year) - number('BD_4', year),
            'businesses_per_1000_people': number('CABEE_5', year) / pop * 1000,
            'house_transfers_per_1000_people': number('HOUSES_2', year) / pop * 1000,
        }
        for key, value in expected.items():
            if math.isnan(value):
                assert r[key] == '', f'{year} {key}: missing values must stay missing'
            else:
                check_close(r[key], value, f'{year} {key}')
    return {
        'sa2_regions': len(score), 'assigned_pois': sum(int(r['poi_count']) for r in score),
        'score_median': statistics.median(scores), 'score_min': min(scores), 'score_max': max(scores),
        'checks': 'density, z-score, sigmoid, rankings, SQL export, SA4 totals, GeoJSON and five ABS indicators agree',
    }


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
