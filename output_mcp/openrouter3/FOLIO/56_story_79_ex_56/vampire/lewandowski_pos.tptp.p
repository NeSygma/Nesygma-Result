% Positive file: Original conclusion as conjecture
fof(striker_robert, axiom, striker(robert_lewandowski)).
fof(strikers_are_players, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_bayern, axiom, left(robert_lewandowski, bayern_munchen)).
fof(leaving_rule, axiom, ! [X, Y] : (left(X, Y) => ~plays_for(X, Y))).
fof(goal, conjecture, plays_for(robert_lewandowski, bayern_munchen)).