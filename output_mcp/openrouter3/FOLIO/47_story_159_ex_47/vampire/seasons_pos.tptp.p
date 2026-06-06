% Positive version: James's favorite season is summer
fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(distinct_students, axiom, (emma != mia & emma != james & mia != james)).
fof(rule_1, axiom, ! [X] : (wants_long_vacation(X) => favorite_season(X, summer))).
fof(fact_emma, axiom, favorite_season(emma, summer)).
fof(fact_mia, axiom, ~favorite_season(mia, summer)).
fof(fact_james, axiom, wants_long_vacation(james)).
fof(goal, conjecture, favorite_season(james, summer)).