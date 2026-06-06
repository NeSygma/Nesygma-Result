fof(lso_is_summer_olympics, axiom, summer_olympics(lso)).
fof(summer_is_sporting, axiom, ! [X] : (summer_olympics(X) => sporting_event(X))).
fof(lso_in_tokyo, axiom, held_in(lso, tokyo)).
fof(us_most_medals_tokyo, axiom, won_most_medals(us, tokyo)).
fof(bridge, axiom, ! [E, C, P] : ((held_in(E, P) & won_most_medals(C, P)) => won_most_medals(C, E))).
fof(goal, conjecture, won_most_medals(us, lso)).