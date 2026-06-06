fof(seasons_are_four, axiom,
    (spring != summer & spring != fall & spring != winter &
     summer != fall & summer != winter & fall != winter)).

fof(has_long_vacation_implies_summer, axiom,
    ! [P] : (wants_long_vacation(P) => favorite_season(P, summer))).

fof(emma_favorite_summer, axiom,
    favorite_season(emma, summer)).

fof(mia_favorite_not_emmas, axiom,
    ? [S] : (favorite_season(mia, S) & S != summer)).

fof(james_wants_long_vacation, axiom,
    wants_long_vacation(james)).

fof(conclusion, conjecture,
    favorite_season(james, summer)).