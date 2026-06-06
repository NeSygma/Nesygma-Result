% Seasons
fof(season_spring, axiom, season(spring)).
fof(season_summer, axiom, season(summer)).
fof(season_fall, axiom, season(fall)).
fof(season_winter, axiom, season(winter)).

% Distinct seasons
fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).

% Premise 2: All students who want a long vacation have summer as favorite season
fof(vacation_rule, axiom, ! [X] : (student(X) & wants_long_vacation(X) => favorite_season(X, summer))).

% Premise 3: Emma's favorite season is summer
fof(emma_fav, axiom, favorite_season(emma, summer)).

% Premise 4: Mia's favorite season is not the same as Emma's (i.e., not summer)
% We'll assert Mia's favorite season is fall (which is not summer)
fof(mia_fav, axiom, favorite_season(mia, fall)).
fof(mia_fav_not_summer, axiom, fall != summer).

% Premise 5: James wants a long vacation
fof(james_wants, axiom, wants_long_vacation(james)).

% Conclusion: James's favorite season is summer
fof(goal, conjecture, favorite_season(james, summer)).