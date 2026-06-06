% Premises about Robert Lewandowski
fof(premise_1, axiom, striker(robert_lewandowski)).
fof(premise_2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise_3, axiom, left(robert_lewandowski, bayern_munchen)).
fof(premise_4, axiom, ! [X,Y] : (left(X,Y) => ~plays_for(X,Y))).

% Conclusion to evaluate
fof(goal, conjecture, soccer_player(robert_lewandowski)).