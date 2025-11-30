import streamlit as st
from pathlib import Path
import pandas as pd

st.title("Aerial Performance Analysis – Serie A 2015/2016")
st.write("Interactive dashboard based on StatsBomb Open Data.")

# -------------------------
# Load Data
# -------------------------
SHOTS_FILE = Path("data/shots_clean.csv")
GAX_FILE = Path("data/player_gax_ranking.csv")

shots = pd.read_csv(SHOTS_FILE)
gax = pd.read_csv(GAX_FILE)

# -------------------------
# Section 1 – GAx Ranking
# -------------------------
st.header("Top 10 Players – Goals Above Expectation (GAx)")

st.image("plots/top10_gax.png", caption="Top 10 GAx – Overall Finishing Efficiency", use_container_width=True)

# -------------------------
# Section 2 – CF Header Goals vs xG vs GAx
# -------------------------
st.header("Center Forwards – Header Goals vs xG vs GAx")

st.image("plots/cf_header_goals_xg_gax.png",
         caption="CF Header Goals vs Header xG vs Header GAx",
         use_container_width=True)

# -------------------------
# Section 3 – CF Top 10 Header Scorers (Scatter)
# -------------------------
st.header("Top 10 CF – Header Conversion Rate")

st.image("plots/top10_header_scorers_cf_scatter.png",
         caption="Conversion Rate vs Attempts (Top 10 CF Header Scorers)",
         use_container_width=True)

# -------------------------
# Section 4 – Explore Player
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
