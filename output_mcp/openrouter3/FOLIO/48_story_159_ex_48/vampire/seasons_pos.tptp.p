% Positive version: Mia's favorite season is spring
fof(seasons_distinct, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(rule_vacation, axiom, ! [P] : (wants_long_vacation(P) => favorite_season(P, summer))).
fof(emma_fav, axiom, favorite_season(emma, summer)).
fof(mia_not_emma, axiom, ~favorite_season(mia, summer)).
fof(james_wants, axiom, wants_long_vacation(james)).
fof(goal, conjecture, favorite_season(mia, spring)).