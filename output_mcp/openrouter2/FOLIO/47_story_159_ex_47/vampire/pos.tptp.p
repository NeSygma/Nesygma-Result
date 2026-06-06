fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(distinct_people, axiom, (emma != mia & emma != james & mia != james)).
fof(long_vacation_rule, axiom, ! [X] : (long_vacation(X) => favorite_season(X, summer))).
fof(favorite_emma, axiom, favorite_season(emma, summer)).
fof(long_vacation_james, axiom, long_vacation(james)).
fof(mia_not_summer, axiom, ~favorite_season(mia, summer)).
fof(conjecture, conjecture, favorite_season(james, summer)).