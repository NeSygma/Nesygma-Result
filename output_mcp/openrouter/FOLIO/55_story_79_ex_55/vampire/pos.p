fof(striker_fact, axiom, striker(robert_lewandowski)).
fof(striker_rule, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_fact, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_rule, axiom, ! [P,T] : (left(P,T) => ~plays_for(P,T))).
fof(goal_pos, conjecture, soccer_player(robert_lewandowski)).