fof(seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(is_season, axiom, ! [S] : (S = spring | S = summer | S = fall | S = winter)).
fof(vacation_rule, axiom, ! [P] : (wants_long_vacation(P) => favorite_season(P, summer))).
fof(emma_fav, axiom, favorite_season(emma, summer)).
fof(mia_fav_diff, axiom, ! [S_mia, S_emma] : ((favorite_season(mia, S_mia) & favorite_season(emma, S_emma)) => S_mia != S_emma)).
fof(james_vacation, axiom, wants_long_vacation(james)).
fof(functional_fav, axiom, ! [P, S1, S2] : ((favorite_season(P, S1) & favorite_season(P, S2)) => S1 = S2)).
fof(person_has_fav, axiom, ! [P] : ? [S] : favorite_season(P, S)).

fof(goal, conjecture, ~favorite_season(mia, spring)).