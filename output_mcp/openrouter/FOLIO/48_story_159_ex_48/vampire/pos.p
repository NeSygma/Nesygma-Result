% Positive run: conjecture that Mia's favorite season is spring
fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(all_long_vac_fav_summer, axiom, ![X] : (wants_long_vacation(X) => favorite(X, summer))).
fof(emma_fav_summer, axiom, favorite(emma, summer)).
fof(mia_fav_not_same_as_emma, axiom, ![S] : ~ (favorite(mia, S) & favorite(emma, S))).
fof(james_wants_long, axiom, wants_long_vacation(james)).
fof(goal, conjecture, favorite(mia, spring)).