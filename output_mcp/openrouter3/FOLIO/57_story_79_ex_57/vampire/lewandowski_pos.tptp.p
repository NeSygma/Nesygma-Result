% Premises about Robert Lewandowski
fof(striker_robert, axiom, striker(robert)).
fof(strikers_are_players, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_bayern, axiom, left_team(robert, bayern)).
fof(leaving_rule, axiom, ! [P, T] : (left_team(P, T) => ~plays_for(P, T))).

% Conclusion to evaluate
fof(goal, conjecture, star(robert)).