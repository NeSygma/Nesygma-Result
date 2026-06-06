fof(robert_is_striker, axiom, striker(robert_lewandowski)).
fof(strikers_are_soccer_players, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(robert_left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(leaving_means_not_playing, axiom, ! [X, Y] : ((soccer_player(X) & left(X, Y)) => ~plays_for(X, Y))).
fof(goal, conjecture, star(robert_lewandowski)).