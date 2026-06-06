% Seasons
fof(season_spring, axiom, season(spring)).
fof(season_summer, axiom, season(summer)).
fof(season_fall, axiom, season(fall)).
fof(season_winter, axiom, season(winter)).

% Distinct seasons
fof(distinct_seasons, axiom, (
    spring != summer & spring != fall & spring != winter &
    summer != fall & summer != winter & fall != winter
)).

% Distinct people
fof(distinct_people, axiom, (
    emma != mia & emma != james & mia != james
)).

% Students
fof(student_emma, axiom, student(emma)).
fof(student_mia, axiom, student(mia)).
fof(student_james, axiom, student(james)).

% Premise 2: All students who want a long vacation have summer as favorite
fof(long_vacation_rule, axiom, ! [X] : (
    (student(X) & wants_long_vacation(X)) => favorite_season(X, summer)
)).

% Premise 3: Emma's favorite season is summer
fof(emma_favorite, axiom, favorite_season(emma, summer)).

% Premise 4: Mia's favorite season is not the same as Emma's (i.e., not summer)
fof(mia_favorite_not_emma, axiom, ~favorite_season(mia, summer)).

% Premise 5: James wants a long vacation
fof(james_wants_vacation, axiom, wants_long_vacation(james)).

% Conclusion: James's favorite season is summer
fof(goal, conjecture, favorite_season(james, summer)).