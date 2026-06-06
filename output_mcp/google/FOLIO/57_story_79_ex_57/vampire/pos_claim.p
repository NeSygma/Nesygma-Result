fof(striker, axiom, is_striker(robert_lewandowski)).
fof(striker_is_player, axiom, ! [X] : (is_striker(X) => is_soccer_player(X))).
fof(left_team, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(left_means_no_play, axiom, ! [P, T] : (left_team(P, T) => ~plays_for(P, T))).
fof(distinct, axiom, robert_lewandowski != bayern_munchen).
fof(goal, conjecture, is_star(robert_lewandowski)).