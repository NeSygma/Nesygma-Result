fof(striker_def, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(lewandowski_is_striker, axiom, striker(robert_lewandowski)).
fof(lewandowski_left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_means_no_play, axiom, ! [P, T] : (left(P, T) => ~plays_for(P, T))).
fof(goal, conjecture, ~plays_for(robert_lewandowski, bayern_munchen)).