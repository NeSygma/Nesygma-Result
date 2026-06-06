fof(striker_robert, axiom, striker(robert)).
fof(strikers_are_players, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(robert_left_bayern, axiom, left(robert, bayern)).
fof(leaves_no_longer_play, axiom, ! [X,Y] : (left(X,Y) => ~plays_for(X,Y))).
fof(conjecture, conjecture, ~soccer_player(robert)).