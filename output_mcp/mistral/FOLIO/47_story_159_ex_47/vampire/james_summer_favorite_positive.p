% Seasons and people types

tff(season_type, type, season: $tType).
tff(person_type, type, person: $tType).

% Declare seasons

% Declare people
tff(emma_decl, type, emma: person).
tff(mi_decl, type, mi: person).
tff(james_decl, type, james: person).

% Declare seasons as constants
tff(spring_decl, type, spring: season).
tff(summer_decl, type, summer: season).
tff(fall_decl, type, fall: season).
tff(winter_decl, type, winter: season).

% Predicates

tff(favorite_season_decl, type, favorite_season: (person * season) > $o).
tff(wants_long_vacation_decl, type, wants_long_vacation: person > $o).

% Premise 1: There are four seasons in a year (implicitly covered by declarations)

% Premise 2: All students who want to have a long vacation have summer as their favorite season
fof(all_long_vacation_lovers_prefer_summer, axiom,
    ! [P: person] : (wants_long_vacation(P) => favorite_season(P, summer))).

% Premise 3: Emma's favorite season is summer
fof(emma_favorite_summer, axiom,
    favorite_season(emma, summer)).

% Premise 4: Mia's favorite season is not the same as Emma's
fof(mia_not_same_as_emma, axiom,
    ? [S: season] : (favorite_season(mi, S) & S != summer)).

% Premise 5: James wants to have a long vacation
fof(james_wants_long_vacation, axiom,
    wants_long_vacation(james)).

% Conclusion to evaluate: James's favorite season is summer
fof(conclusion_james_summer_favorite, conjecture,
    favorite_season(james, summer)).