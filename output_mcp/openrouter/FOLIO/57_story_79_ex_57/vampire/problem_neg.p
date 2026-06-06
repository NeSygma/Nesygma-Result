% Negative version
fof(distinct, axiom, robert_lewandowski != bayern_munchen).
fof(a1, axiom, striker(robert_lewandowski)).
fof(a2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(a3, axiom, left(robert_lewandowski, bayern_munchen)).
fof(a4, axiom, ! [P,T] : (left(P,T) => ~plays_for(P,T))).
fof(goal_neg, conjecture, ~star(robert_lewandowski)).