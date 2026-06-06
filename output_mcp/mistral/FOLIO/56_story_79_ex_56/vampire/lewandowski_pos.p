fof(robert_is_striker, axiom, striker(robert_lewandowski)).
fof(striker_implies_soccer_player, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(robert_left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_implies_not_plays_for, axiom, ! [X, T] : (left(X, T) => ~plays_for(X, T))).
fof(conclusion, conjecture, plays_for(robert_lewandowski, bayern_munchen)).