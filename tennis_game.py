# MVP Tennis Game Scoreboard
# tracks a full match with scores per game, sets, match winner and 
# correct 'tennis terminology'

#region Class:TennisGame
class TennisGame:
    def __init__(self, player_names=None):
        # Point score for current game:
        self.scores = {'A': 0, 'B' : 0}
        # Total points for each player in a match
        self.total_points = {'A': 0, 'B': 0}
        #Player display names
        self.player_names = player_names or {'A': 'Player A', 'B': 'Player B'}
        # Tennis score labels 'tennis lingo' for points
        self.score_names = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}
        #History of completed sets for display
        self.set_history = []
        # Set counter ("Set No.") refactored?
        self.set_number = 1
        # Tracks how many games each player has won in current set
        self.games_won = {'A': 0, 'B': 0}
        #Tracks how many sets each player has won in the match
        self.sets_won = {'A': 0, 'B': 0}
        # Tie-break
        self.in_tiebreak = False
        self.tiebreak_scores = {'A': 0, 'B': 0}

    def get_name(self, player):
        #Returns display name for a player
        return self.player_names.get(player, player)
    
    def player_names_list(self):
        # Refactor/shortcut to get both player names
        return [self.get_name('A'), self.get_name('B')]
#endregion

#region Scoring
    def score(self):
        #Returns current game score as string. regular game
        player_a, player_b = self.player_names_list()

        if self.in_tiebreak:
            a, b = self.tiebreak_scores['A'], self.tiebreak_scores['B']
            return f"Tiebreak: {player_a} {a} - {b} {player_b}"
        
        a, b = self.scores['A'], self.scores['B']

        def score_label(points):
            return self.score_names.get(points, "Fourty+")

        # if a tie in the game occurs
        if a == b:
            if a == 0:
                return "Love - All"
            elif a in [1, 2]:
                return f"{score_label(a)}- All"
            else:
                return "Deuce"
        
        # marker for 'Advantage' and win
        if a >= 4 or b >= 4:
            if abs(a - b) == 1:
                return f"Advantage {player_a if a > b else player_b}"
            elif abs(a - b) >= 2:
                return (
                    f"Win for {player_a if a > b else player_b}"
                    f"- Final Score: {score_label(a)} - {score_label(b)}"
                )
        # Score format
        return f"{score_label(a)} - {score_label(b)}"

    # Updates scores + point  + check for tiebreak
    def point_won_by(self, player):
        if self.in_tiebreak:
            self.tiebreak_scores[player] += 1
            self.check_tiebreak()
        else:    
            self.scores[player] += 1
            self.total_points[player] += 1
            # Check if game or match is ending
            self.check_game()
            self.check_match()
#endregion

#region Match Control
#---- Check if a game is won --------#    
    def check_game(self):
        a, b = self.scores['A'], self.scores['B']
        if (a >= 4 or b >= 4) and abs(a-b) >= 2:
            winner = 'A' if a>b else 'B'
            self.games_won[winner] += 1
            self.scores = {'A': 0, 'B': 0} # Reset game score
            self.check_set() # Check if it is the end of the set?

#---- Check if a set is over -----#
    def check_set(self):
        a, b, = self.games_won['A'], self.games_won['B']

#tiebreak at 6-6
        if a == 6 and b ==6:
            self.in_tiebreak = True
            self.tiebreak_scores = {'A': 0, 'B': 0}
            return

#regular set conditions:
        if (a >= 6 or b >= 6) and abs(a - b) >= 2:
            winner = 'A' if a > b else 'B'
            winner_name = self.get_name(winner)

            #Log completion
            self.set_history.append({
                "set": self.set_number,
                "A": a,
                "B": b,
                "note": f"Win for: {winner_name}"
            })
            #reset for next set
            self.set_number +=1
            self.sets_won[winner] +=1
            self.games_won = {'A': 0, 'B': 0}

# ----- Check for tiebreak method----
    def check_tiebreak(self):
        a, b = self.tiebreak_scores['A'], self.tiebreak_scores['B']
        if (a >= 7 or b >= 7) and abs(a-b) >=2:
            winner = 'A' if a>b else 'B'
            winner_name = self.get_name(winner)

            self.set_history.append({
                "set": self.set_number,
                "A": self.games_won['A'],
                "B": self.games_won['B'],
                "note": f"Win for: {winner_name} (Tiebreak {a}-{b})"
            })
            self.sets_won[winner] += 1
            self.set_number += 1
            self.games_won = {'A': 0, 'B': 0}
            self.in_tiebreak = False


#---- Check if a match is over-----#
    def check_match(self):
        return self.match_winner() is not None

#------Returns winner of the match------
    def match_winner(self):
        if self.sets_won['A'] == 2:
            return self.get_name('A')
        elif self.sets_won['B'] == 2:
            return self.get_name('B')
        return None
#endregion


