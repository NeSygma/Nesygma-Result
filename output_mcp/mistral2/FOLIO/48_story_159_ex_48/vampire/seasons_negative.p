fof(seasons_distinct, axiom,
    (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).

fof(long_vacation_implies_summer, axiom,
    ! [P] : (wants_long_vacation(P) => favorite_season(P, summer))).

fof(emma_favorite_summer, axiom,
    favorite_season(emma, summer)).

fof(mia_not_same_as_emma, axiom,
    ! [S] : (favorite_season(mia, S) => S != summer)).

fof(james_wants_long_vacation, axiom,
    wants_long_vacation(james)).

fof(goal_negation, conjecture,
    ~favorite_season(mia, spring)).