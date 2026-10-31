# 悉尼 POI 空间分布与城市资源分析

本项目把 NSW 政府 POI 数据与 ABS 的 SA2 边界结合起来，分析悉尼四个 SA4 区域内的设施分布和资源集中程度。它是 DATA2001 的 Group31 团队项目，仓库展示团队已有代码、报告和结果，不把团队成果写成个人独立完成。

## 可以直接查看的成果

- [完整分析 notebook](../notebooks/sydney_poi_analysis.ipynb)：Pandas 清洗、API 获取、GeoPandas 几何处理、PostGIS 数据库和评分。
- [项目报告](../reports/sydney_poi_report.pdf)：保留原分析内容，删除重复方法页和空白尾页。
- [空间分布地图](../results/figures/well_resourced_score_map.png)与[交互地图文件](../results/maps/interactive_well_resourced_score_map.html)。交互地图需下载后用浏览器打开。
- [全部 SA2 评分](../results/tables/well_resourced_score_by_sa2.csv)、前十和后十排名、POI 分类统计与 NSW 年度指标。
- [SQL 空间匹配](../sql/spatial_assignment.sql)和[SQL 评分计算](../sql/score_calculation.sql)。

## 做了什么

先用 SA2 的矩形范围查询 API，得到 18,209 行记录；去重和清理后留下 10,627 个 POI，再通过 `ST_Within` 判断点是否真正落在区域内，得到 9,042 个有效 POI。对 128 个 SA2 计算每平方公里 POI 数，将密度标准化，再通过 sigmoid 转换为 0–1 的评分。

代码也清理了 ABS 2019–2024 年的 NSW 数据，计算人口增长、女性与男性人口比、自然增长、每千人企业数和每千人住宅交易数。

## 得出的结论

研究区内 POI 密度差异明显。Sydney (North) – Millers Point 最高，评分约 0.993、密度约 98.37 个/km²；Banksmeadow 最低，评分约 0.242。中位数约 0.428。

这个评分衡量设施的空间集中程度。工业区、机场、绿地面积、跨区域使用设施和真实交通时间都会影响解释，因此不能直接把分数当作生活质量排名。NSW 的全州趋势也不能证明悉尼某个街区的企业增长。

## 为什么保留 CSV 和 README

README 是别人打开仓库时看到的项目首页，负责解释问题、方法、成果和运行方式。CSV 是能直接检查的结果和复现输入，因此值得保留。全国 70 MB 的边界文件已用 128 区域的完整几何子集替代。作业题目 PDF、重复草稿、原 ZIP 和系统文件不进入仓库。

一个 `main` 分支已经足够。当前 Git 提交记录如实反映本次整理，没有伪造过去的开发过程。

## 结果核验

```bash
python scripts/verify_results.py
python -m pip install "shapely>=2,<3"
python scripts/verify_spatial_join.py
```

以上脚本已在本地通过：复核了评分公式、排名、地图数据、五项统计，并独立重做空间匹配，128 个区域的数量全部与原数据库导出一致。完整数据库 notebook 没有在本次整理中重跑。

原 notebook 有一段后来加入的人口过滤代码，保留 123 个区域，但报告和已导出的地图仍是 128 个区域。本仓库统一采用报告的 128 区域口径，并保留独立审计文件，具体见[复现说明](reproducibility.md)。
