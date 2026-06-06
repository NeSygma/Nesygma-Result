fof(premise1, axiom, striker(robert)).
fof(premise2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise3, axiom, left(robert, bayern)).
fof(premise4, axiom, ! [X, Y] : (left(X, Y) => ~plays_for(X, Y))).
fof(goal, conjecture, plays_for(robert, bayern)).