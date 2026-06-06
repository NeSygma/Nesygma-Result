fof(p1, axiom, striker(robert_lewandowski)).
fof(p2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(p3, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(p4, axiom, ! [P, T] : (left_team(P, T) => ~plays_for(P, T))).
fof(goal, conjecture, ~soccer_player(robert_lewandowski)).