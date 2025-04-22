import streamlit as st
from tennis_game import TennisGame

#----Player selection dropdown------#
def player_selection(player_key, other_player_key, label, players):
    available = [p for p in players if p != st.session_state[other_player_key] or p== players[0]]
    default_index =(
        available.index(st.session_state[player_key])
        if st.session_state[player_key] in available
        else 0
    )
    st.selectbox(label, available, index = default_index, key= player_key)


#------ Selected player button logic ----#
def point_button(col, player_key, default_label, player_id, players):
    player_name = st.session_state[player_key]
    label = f"Click to Play: {player_name}" if player_name != players[0] else f"Click to Play: {default_label}"
    with col:
        if player_name == players[0] or st.session_state.game.check_match():
            st.button(label, disabled = True)
        else:
            if st.button(label):
                player_id = player_key[-1].upper()
                st.session_state.game.point_won_by(player_id)
