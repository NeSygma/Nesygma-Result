fof(premise1, axiom, striker(robert)).
fof(premise2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise3, axiom, left(robert, bayern_munchen)).
fof(premise4, axiom, ! [X,T] : (left(X,T) => ~plays_for(X,T))).
fof(distinct, axiom, robert != bayern_munchen).
fof(conjecture, conjecture, star(robert)).