# Findings and interpretation

The report snapshot covers 128 SA2s in Sydney – Parramatta, Sydney – Inner South West, Sydney – City and Inner South, and Sydney – North Sydney and Hornsby. It is a selected-region study, not a ranking of all Greater Sydney.

## Spatial concentration

After deduplication and exact spatial assignment, 9,042 POIs fall within the study polygons. The score distribution has a median of 0.42799 and a range of 0.24191–0.99319. Millers Point and Sydenham – Tempe – St Peters have the highest density-based scores. Banksmeadow has the lowest.

Raw totals and density answer different questions. Inner South West has the largest SA4 POI total, while the highest-scoring individual SA2 is in City and Inner South. A small polygon with concentrated POIs can rank highly without the largest absolute POI count.

## NSW indicators

Five indicators were calculated from the ABS source CSV: population growth, female-to-male population ratio, natural increase, businesses per 1,000 people and established-house transfers per 1,000 people. The main time window is 2019–2024; missing source values remain missing.

- Population growth is about 2.14% in 2023 and 1.66% in 2024.
- Businesses per 1,000 residents rise from 96.94 in 2020 to 105.73 in 2024.
- Natural increase falls from 44,807 in 2021 to 32,496 in 2023.
- Established-house transfers per 1,000 residents peak at about 15.58 in 2021, fall to 10.34 in 2023 and recover to 11.35 in 2024.

These indicators describe NSW. They cannot show that business growth was concentrated in specific Sydney SA2s. The original report's discussion makes a stronger spatial inference about growth than these data support; that inference should not be used as a project finding.

## Limits of the score

1. Every POI has equal weight. Facility size, service quality and capacity are omitted.
2. POIs/km² is an area-based concentration measure. Population is not its denominator.
3. SA2 boundaries introduce MAUP and exclude access to facilities just across a border.
4. Large parkland areas can lower density; industrial and airport zones are not comparable with residential suburbs.
5. The API snapshot may omit facilities or contain coordinate errors. The original collection function did not paginate. Live refresh now rejects responses flagged as truncated, but the saved snapshot's completeness is not established.
6. No travel-time, public-transport, causal, or longitudinal SA2 model was fitted.

The useful conclusion is that recorded POI density varies across this study area. Assessing actual resident accessibility would require demand, capacity and transport-network information.
