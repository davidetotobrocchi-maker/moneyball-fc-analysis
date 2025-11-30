import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------
# Load Data
# -------------------------
SHOTS_FILE = Path("data/shots_clean.csv")
GAX_FILE = Path("data/player_gax_ranking.csv")

st.title("Aerial Performance Analysis – Serie A 2015/2016")
st.write("Interactive dashboard based on StatsBomb Open Data.")

# Load datasets
shots = pd.read_csv(SHOTS_FILE)
gax = pd.read_csv(GAX_FILE)

# -------------------------
# Section 1 – GAx Ranking
# -------------------------
st.header("Top 10 Players – Goals Above Expectation (GAx)")

top10_gax = gax.sort_values("gax", ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(top10_gax["player.name"], top10_gax["gax"])
plt.xticks(rotation=45, ha="right")
st.pyplot(fig1)

# -------------------------
# Section 2 – Header Conversion (CF Only)
# -------------------------
st.header("Center Forward – Header Conversion Rate")

cf = shots[shots["shot.body_part.name"] == "Head"].copy()
cf_stats = cf.groupby("player.name").agg(
    headers=("player.name", "count"),
    goals=("is_goal", "sum"),
).reset_index()

cf_stats["conversion"] = cf_stats["goals"] / cf_stats["headers"]

top10_conv = cf_stats.sort_values("goals", ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.scatter(
    top10_conv["headers"], 
    top10_conv["conversion"],
    s=top10_conv["goals"] * 150,
    color="#1f77b4"
)
for _, r in top10_conv.iterrows():
    ax2.text(r["headers"], r["conversion"], r["player.name"], fontsize=8)

ax2.set_xlabel("Header Attempts")
ax2.set_ylabel("Conversion Rate")
st.pyplot(fig2)

# -------------------------
# Section 3 – Explore a Player
# -------------------------
st.header("Explore a Player")

player_list = sorted(shots["player.name"].dropna().unique())
choice = st.selectbox("Select Player", player_list)

player_shots = shots[shots["player.name"] == choice]

col1, col2, col3 = st.columns(3)
col1.metric("Total Shots", len(player_shots))
col2.metric("Goals", player_shots["is_goal"].sum())
col3.metric("Total xG", round(player_shots["shot.statsbomb_xg"].sum(), 2))

st.write("Shot Details:")
st.dataframe(player_shots)
