% Positive test: original claim as conjecture
fof(premise_1, axiom, striker(robert_lewandowski)).
fof(premise_2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise_3, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(premise_4, axiom, ! [X, Y] : (left_team(X, Y) => ~plays_for(X, Y))).
fof(conjecture, conjecture, soccer_player(robert_lewandowski)).