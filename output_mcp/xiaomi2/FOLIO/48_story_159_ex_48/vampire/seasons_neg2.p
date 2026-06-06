% Domain: four seasons
fof(seasons_distinct, axiom,
    (spring != summer & spring != fall & spring != winter &
     summer != fall & summer != winter & fall != winter)).

% Each person has exactly one favorite season (uniqueness)
fof(fav_unique, axiom, ! [P, S1, S2] :
    ((favorite_season(P, S1) & favorite_season(P, S2)) => S1 = S2)).

% Premise: All who want long vacation => favorite season is summer
fof(long_vacation_rule, axiom, ! [X] :
    (wants_long_vacation(X) => favorite_season(X, summer))).

% Premise: Emma's favorite season is summer
fof(emma_fav, axiom, favorite_season(emma, summer)).

% Premise: Mia's favorite season is not the same as Emma's
fof(mia_not_summer, axiom, ~favorite_season(mia, summer)).

% Premise: James wants a long vacation
fof(james_wants, axiom, wants_long_vacation(james)).

% Negated conclusion: Mia's favorite season is NOT spring
fof(goal, conjecture, ~favorite_season(mia, spring)).