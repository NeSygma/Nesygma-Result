fof(robert_is_striker, axiom, striker(robert_lewandowski)).
fof(strikers_are_soccer_players, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(robert_left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_means_no_longer_play, axiom, ! [X, T] : ((soccer_player(X) & left(X, T)) => ~plays_for(X, T))).
fof(goal, conjecture, ~star(robert_lewandowski)).