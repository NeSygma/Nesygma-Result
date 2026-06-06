% Positive version
fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(all_long_vacation, axiom, ![X] : (wants_long_vacation(X) => favorite(X, summer))).
fof(emma_fav, axiom, favorite(emma, summer)).
fof(mia_not_same, axiom, ~favorite(mia, summer)).
fof(james_wants, axiom, wants_long_vacation(james)).
fof(goal, conjecture, favorite(james, summer)).