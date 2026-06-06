fof(premise_1, axiom, striker(robert_lewandowski)).
fof(premise_2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise_3, axiom, left(robert_lewandowski, bayern_munchen)).
fof(premise_4, axiom, ! [X, Y] : ((soccer_player(X) & left(X, Y)) => ~plays_for(X, Y))).
fof(goal, conjecture, ~plays_for(robert_lewandowski, bayern_munchen)).