fof(striker_robert, axiom, striker(robert_lewandowski)).
fof(striker_is_player, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_robert, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_implies_not_plays, axiom, ! [X,Y] : (left(X,Y) => ~plays_for(X,Y))).
fof(distinct_robert_bayern, axiom, robert_lewandowski != bayern_munchen).
fof(conjecture, conjecture, plays_for(robert_lewandowski, bayern_munchen)).