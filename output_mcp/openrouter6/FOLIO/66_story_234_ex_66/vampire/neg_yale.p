fof(axiom1, axiom, private(yale) & ivy_league(yale) & research(yale)).
fof(axiom2, axiom, moved_to_new_haven(yale)).
fof(goal, conjecture, ! [X] : (~private(X) | ~ivy_league(X) | ~research(X) | ~moved_to_new_haven(X))).