fof(is_striker_robert, axiom, is_striker(robert_lewandowski)).
fof(striker_are_players, axiom, ! [P] : (is_striker(P) => is_soccer_player(P))).
fof(robert_left_bayern, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(left_implies_not_plays_for, axiom, ! [P, T] : (left_team(P, T) => ~plays_for(P, T))).
fof(conclusion, conjecture, is_soccer_player(robert_lewandowski)).