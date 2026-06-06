fof(distinct_seasons, axiom,
    (spring != summer & spring != fall & spring != winter &
     summer != fall & summer != winter &
     fall != winter)).
fof(distinct_persons, axiom,
    (emma != mia & emma != james & mia != james)).
fof(premise1, axiom, season(spring)).
fof(premise1b, axiom, season(summer)).
fof(premise1c, axiom, season(fall)).
fof(premise1d, axiom, season(winter)).
fof(premise2, axiom,
    ! [X] : ((student(X) & wants_long_vacation(X)) => favorite_season(X, summer))).
fof(premise3, axiom, favorite_season(emma, summer)).
fof(premise4, axiom,
    ? [S] : (season(S) & favorite_season(mia, S) & S != summer)).
fof(premise5, axiom, wants_long_vacation(james)).
fof(conclusion_negated, conjecture, ~favorite_season(james, summer)).