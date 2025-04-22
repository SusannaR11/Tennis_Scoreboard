import streamlit as st
import pandas as pd
from tennis_game import TennisGame
from ui_utilities import player_selection, point_button

# --- Streamlit UI ---
st.title("🎾 Bilvision Cup")
st.title("Tennis Scoreboard")

# ---- Player pool from CSV-files----#
#players = ['- Select from dropdown -', 'Roger Federer', 'Rafael Nadal', 'Novak Djokovic', 'Serena Williams', 'Steffi Graf', 'Martina Navratilova']
male_player_path = "data/male_players.csv"
male_players_from_csv = pd.read_csv(male_player_path).squeeze().tolist()
players = [' - Select from dropdown - '] + male_players_from_csv

#--- init session state -----#
for key in ["player_a", "player_b"]:
    if key not in st.session_state:
        st.session_state[key] = players[0]

#---- dropdown menus -----#
st.markdown(" ## Choose your player")
player_selection("player_a", "player_b", "Select Player A", players)
player_selection("player_b", "player_a", "Select Player B", players)

#---- initialize game--------
if (
    st.session_state.player_a != players[0]
    and st.session_state.player_b != players[0]
    and "game" not in st.session_state
    ):
    st.session_state.game = TennisGame({
        'A': st.session_state.player_a,
        'B': st.session_state.player_b
    })
#----- get game ---------
game = st.session_state.get("game")
#----- Retrieve player names -------
if game:
    player_a, player_b = game.player_names_list()
#-------Point buttons-------
    col1, col2 = st.columns(2)
    point_button(col1, "player_a", "Player A", "A", players)
    point_button(col2, "player_b", "Player B", "B", players)


#------Current score------   
    st.markdown("#### Current Score")
    st.markdown(f"#### `{game.score()}`")

    st.markdown("#### Games & Sets")
    st.write(f"Games: {player_a} {game.games_won['A']} - {game.games_won['B']} {player_b}")
    st.write(f"Sets: {player_a} {game.sets_won['A']} - {game.sets_won['B']} {player_b}")

#------Set History--------
    if game.set_history:
        st.markdown("#### Set History")
        set_table = pd.DataFrame([
            {
                player_a: s["A"],
                player_b: s["B"],
                "Notes": s["note"]
            }
            for s in game.set_history
        ])
        set_table.index = range(1, len(set_table) + 1)
        set_table.index.name = "Set No."
        st.table(set_table)

#----Functionality for downloading historical match data-----   
    #csv = set_table.to_csv().encode('utf-8')
    #st.download_button(
        #label="Download Match History as CSV",
        #data=csv,
        #file_name='match_history.csv',
        #mime='text/csv')


#----Display match winner-----
    if game.check_match():
        st.markdown(f"### Match Winner: **{game.match_winner()}**")

#------Reset button for Game--------
if st.button("Reset Game"):
    if (
        st.session_state.player_a != players[0]
        and st.session_state.player_b != players[0]
    ):
        st.session_state.game = TennisGame({
            'A': st.session_state.player_a,
            'B': st.session_state.player_b
    })

#---- Reset button for Match-------
if st.button("Reset Match"):
    st.session_state.game = TennisGame({
        'A': st.session_state.player_a,
        'B': st.session_state.player_b
    })