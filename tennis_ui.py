import streamlit as st
import pandas as pd
from tennis_game import TennisGame
from ui_utilities import player_selection, point_button

# --- Streamlit UI ---
st.title("🎾 Tennis Open 2025")
st.title("🌺 Tournament 🌺")
st.markdown("## Scoreboard")


# ---- Player pool from CSV-files----#
#players = ['- Select from dropdown -', 'Roger Federer', 'Rafael Nadal', 'Novak Djokovic', 'Serena Williams', 'Steffi Graf', 'Martina Navratilova']
#sort by last name in dropdown
def sort_by_last_name(name):
    return name.split()[-1]

male_player_path = "data/male_players.csv"
female_player_path = "data/female_players.csv"

male = pd.read_csv(male_player_path).squeeze().tolist()
female = pd.read_csv(female_player_path).squeeze().tolist()
#combine players into a mixed list
all_players_from_csv = sorted(set(male + female), key=sort_by_last_name)
players = [' - Select from dropdown - '] + all_players_from_csv

#--- init session state -----#
for key in ["player_a", "player_b"]:
    if key not in st.session_state:
        st.session_state[key] = players[0]

#---- dropdown menus -----#
st.markdown(" ### Choose your player -")
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

#------Tiebreak flag------
    if game.in_tiebreak:
        st.markdown("##### Tiebreak")

#------Current score------   
    st.markdown("#### Current Score")
    st.markdown(f"#### `{game.score()}`")

    st.markdown("#### Game")
    st.write(f"{player_a} {game.games_won['A']} - {game.games_won['B']} {player_b}")

#------Set History--------
    if game.set_history:
        st.markdown("#### Score")

        sets_data = {
            player_a: [],
            player_b: []
        }

        for s in game.set_history:
            note = s.get("note", "") #list of 

            a_score = f"{s['A']}"
            b_score = f"{s['B']}"

            if "Tiebreak" in note:
                tb_score = note.split("Tiebreak")[-1].strip(" )(")
                tiebreak_a, tiebreak_b = tb_score.split("-")
                if s['A'] > s['B']:
                    a_score += f"({tiebreak_a})"
                    b_score += f"({tiebreak_b})"
                else:
                    a_score += f"({tiebreak_b})"
                    b_score += f"({tiebreak_a})"

            sets_data[player_a].append(a_score)
            sets_data[player_b].append(b_score)

        set_df = pd.DataFrame(sets_data).T #transpose
        set_df.columns = [f"Set {i+1}" for i in range(len(game.set_history))]

        st.table(set_df)


      #  set_table = pd.DataFrame([
     #       {
      #          player_a: s["A"],
       #         player_b: s["B"],
      #          "Notes": s["note"]
      #      }
      #      for s in game.set_history
      #  ])
      #  set_table.index = range(1, len(set_table) + 1)
      #  set_table.index.name = "Set No."
      #  st.table(set_table)

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