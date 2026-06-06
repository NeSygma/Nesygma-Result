fof(seasons_distinct, axiom,
    ( spring != summer & spring != fall & spring != winter &
      summer != fall & summer != winter & fall != winter )).

fof(people_distinct, axiom,
    ( emma != mia & emma != james & mia != james )).

% All students who want a long vacation have summer as favorite season
fof(long_vacation_rule, axiom,
    ! [X] : (wants_long_vacation(X) => favorite_season(X, summer))).

% Emma's favorite season is summer
fof(emma_fav, axiom, favorite_season(emma, summer)).

% Mia's favorite season is not the same as Emma's (i.e., not summer)
fof(mia_fav_not_summer, axiom, ~favorite_season(mia, summer)).

% James wants a long vacation
fof(james_wants, axiom, wants_long_vacation(james)).

% Negated conclusion: James's favorite season is NOT summer
fof(goal, conjecture, ~favorite_season(james, summer)).