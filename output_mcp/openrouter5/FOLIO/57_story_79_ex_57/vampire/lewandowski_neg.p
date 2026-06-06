fof(striker_fact, axiom, striker(robert_lewandowski)).
fof(striker_to_player, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_fact, axiom, left(robert_lewandowski, bayern_munchen)).
fof(left_implies_no_longer_plays, axiom, ! [X, Y] : (left(X, Y) => ~plays_for(X, Y))).
fof(goal, conjecture, ~star(robert_lewandowski)).