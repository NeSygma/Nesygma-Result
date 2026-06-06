fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(vacation_fav, axiom, ! [X] : (wants_long_vacation(X) => favorite_season(X, summer))).
fof(emma_fav, axiom, favorite_season(emma, summer)).
fof(mia_not_emma, axiom, ~favorite_season(mia, summer)).
fof(james_vacation, axiom, wants_long_vacation(james)).
fof(goal, conjecture, favorite_season(mia, spring)).