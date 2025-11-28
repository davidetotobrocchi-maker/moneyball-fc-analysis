# moneyball-fc-analysis
This project applies a data-driven “Moneyball” approach to football analytics using StatsBomb Open Data. The focus of the study is the aerial performance of center forwards (CFs) in Serie A during the 2015/2016 season, with particular attention to:

Goals scored with headers
Expected Goals on header attempts (xG)
Goals Above Expectation (GAx) on headers -> GAx = Goals – xG
Shooting efficiency and conversion

The goal is to support evidence-based scouting by identifying strikers who excel in aerial finishing or who may be undervalued relative to their underlying metrics.


The project uses the publicly available StatsBomb Open Data:
Event data (shots, body parts, outcomes)
Lineups (used to identify player positions)
Match information
Competition information 

From these datasets, all shots from Serie A 2015/2016 were extracted and filtered to isolate:
Only players with more than 20 shots
Only shot events
Only header attempts
Only players assigned to center-forward positions in at least one match


Analysis Outputs
The project generates multiple visual insights, including:

Top 10 players by GAx (overall finishing efficiency)
Top aerial finishers among Serie A center forwards
Comparison of goals vs xG vs GAx on headers
(to distinguish sustainable performers from overperformers)

