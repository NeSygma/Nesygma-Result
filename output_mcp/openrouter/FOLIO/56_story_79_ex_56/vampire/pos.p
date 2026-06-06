fof(p1, axiom, striker(robert_lewandowski)).
fof(p2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(p3, axiom, left(robert_lewandowski, bayern_munchen)).
fof(p4, axiom, ! [P,T] : (left(P,T) => ~plays_for(P,T))).
fof(distinct, axiom, robert_lewandowski != bayern_munchen).
fof(goal, conjecture, plays_for(robert_lewandowski, bayern_munchen)).