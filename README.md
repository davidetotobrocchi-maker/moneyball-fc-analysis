# moneyball-fc-analysis
This project applies a Moneyball-inspired, data-driven approach to football analytics using StatsBomb Open Data.
The focus is the aerial performance of center forwards in Serie A during the 2015/2016 season, with the goal of supporting scouting for teams that rely heavily on crosses.
By analysing headed goals, expected goals, efficiency, and shot volume, the study aims to identify which strikers are truly effective in the air and which players may be undervalued relative to their underlying metrics.

The analysis examines:
-Goals scored with headers
-Expected Goals on header attempts (xG)
-Goals Above Expectation (GAx = Goals − xG)
-Header conversion efficiency
-Shooting volume and consistency

Data Sources;
The project uses the publicly available StatsBomb Open Data, including:
-Event data (shots, body parts, outcomes)
-Lineups (used to determine whether a player acted as a center forward)
-Matches and competitions information

From these datasets, the analysis extracts and filters:
-Only Serie A 2015/2016 matches
-Only shot events
-Only header attempts
-Only players who appeared as center forwards

Additional filtering for certain visualizations:
-Players with more than 20 total shots
-Players with ≥ 10 header attempts
-Players with ≥ 3 header goals

Conclusion
The analysis highlights clear differences in the aerial performance of Serie A center forwards during the 2015/2016 season. Alberto Gilardino emerges as the most productive and consistent header finisher, combining high goal output with one of the highest xG values. Leonardo Pavoletti also shows strong reliability, generating many aerial attempts and converting them at a stable rate. In contrast, players like Filip Djordjević display excellent efficiency but on too few attempts to be considered sustainable over time.
Overall, the results indicate that forwards who pair high attempt volume with matching or above-expected efficiency—such as Gilardino and Pavoletti—represent the most dependable aerial profiles for teams looking to improve their scoring ability from crosses.