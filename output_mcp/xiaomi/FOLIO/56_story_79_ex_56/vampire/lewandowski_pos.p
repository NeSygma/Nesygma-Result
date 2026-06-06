fof(striker_lewandowski, axiom, striker(robert_lewandowski)).
fof(striker_is_player, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_means_not_playing, axiom, ! [X, Y] : ((soccer_player(X) & left(X, Y)) => ~plays_for(X, Y))).
fof(goal, conjecture, plays_for(robert_lewandowski, bayern_munchen)).