fof(robert_is_striker, axiom, striker(robert_lewandowski)).
fof(striker_implies_soccer_player, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(robert_left_bayern, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(left_team_implies_not_plays_for, axiom, ! [P, T] : (left_team(P, T) => ~plays_for(P, T))).
fof(conclusion_not_star, conjecture, ~star(robert_lewandowski)).