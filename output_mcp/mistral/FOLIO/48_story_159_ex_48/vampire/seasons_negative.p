fof(seasons_distinct, axiom,
    (spring != summer & spring != fall & spring != winter &
     summer != fall & summer != winter &
     fall != winter)).

fof(wants_vacation_implies_summer, axiom,
    ! [P] : (wants_long_vacation(P) => favorite_season(P, summer))).

fof(emma_favorite_summer, axiom,
    favorite_season(emma, summer)).

fof(mia_not_summer, axiom,
    ~favorite_season(mia, summer)).

fof(james_wants_vacation, axiom,
    wants_long_vacation(james)).

fof(unique_favorite, axiom,
    ! [P, S1, S2] : ((favorite_season(P, S1) & favorite_season(P, S2)) => S1 = S2)).

fof(emma_has_favorite, axiom,
    ? [S] : favorite_season(emma, S)).

fof(mia_has_favorite, axiom,
    ? [S] : favorite_season(mia, S)).

fof(james_has_favorite, axiom,
    ? [S] : favorite_season(james, S)).

fof(conclusion_negation, conjecture,
    ~favorite_season(mia, spring)).