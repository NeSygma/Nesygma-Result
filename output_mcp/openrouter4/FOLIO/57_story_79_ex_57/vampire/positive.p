fof(premise1, axiom, striker(robert_lewandowski)).
fof(premise2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise3, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(premise4, axiom, ! [X, T] : (left_team(X, T) => no_longer_plays_for(X, T))).
fof(goal, conjecture, star(robert_lewandowski)).