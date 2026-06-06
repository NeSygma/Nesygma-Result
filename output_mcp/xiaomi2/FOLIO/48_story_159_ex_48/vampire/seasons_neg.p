% Domain: seasons
fof(seasons_domain, axiom, ! [S] : (S = spring | S = summer | S = fall | S = winter)).
fof(seasons_distinct, axiom,
    (spring != summer & spring != fall & spring != winter &
     summer != fall & summer != winter & fall != winter)).

% Each person has exactly one favorite season
fof(fav_exists, axiom, ! [P] : ? [S] : favorite_season(P, S)).
fof(fav_unique, axiom, ! [P, S1, S2] :
    ((favorite_season(P, S1) & favorite_season(P, S2)) => S1 = S2)).

% Premise 2: All who want long vacation => favorite season is summer
fof(long_vacation_rule, axiom, ! [X] :
    (wants_long_vacation(X) => favorite_season(X, summer))).

% Premise 3: Emma's favorite season is summer
fof(emma_fav, axiom, favorite_season(emma, summer)).

% Premise 4: Mia's favorite season is not the same as Emma's (i.e., not summer)
fof(mia_not_summer, axiom, ~favorite_season(mia, summer)).

% Premise 5: James wants a long vacation
fof(james_wants, axiom, wants_long_vacation(james)).

% Negated conclusion: Mia's favorite season is NOT spring
fof(goal, conjecture, ~favorite_season(mia, spring)).