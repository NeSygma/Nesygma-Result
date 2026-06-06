fof(robert_is_striker, axiom, striker(robert_lewandowski)).
fof(striker_are_players, axiom, ! [P] : (striker(P) => soccer_player(P))).
fof(robert_left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_implies_not_plays_for, axiom, ! [P, T] : (left(P, T) => ~plays_for(P, T))).
fof(conclusion, conjecture, plays_for(robert_lewandowski, bayern_munchen)).