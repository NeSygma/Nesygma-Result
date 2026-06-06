fof(seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(is_season, axiom, ! [S] : (S = spring | S = summer | S = fall | S = winter)).
fof(vacation_rule, axiom, ! [P] : (wants_long_vacation(P) => favorite_season(P, summer))).
fof(emma_fav, axiom, favorite_season(emma, summer)).
fof(mia_fav, axiom, ! [S1, S2] : ((favorite_season(mia, S1) & favorite_season(emma, S2)) => S1 != S2)).
fof(james_wants, axiom, wants_long_vacation(james)).
fof(goal, conjecture, ~favorite_season(james, summer)).