% Negative version: negated conclusion as conjecture
% Premises:
% 1. There are four seasons: Spring, Summer, Fall, Winter
fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).

% 2. All students who want to have a long vacation have summer as their favorite season.
fof(rule_long_vacation, axiom, ! [X] : (wants_long_vacation(X) => favorite_season(X, summer))).

% 3. Emma's favorite season is summer.
fof(emma_favorite, axiom, favorite_season(emma, summer)).

% 4. Mia's favorite season is not the same as Emma's.
fof(mia_not_emma, axiom, ! [S] : (favorite_season(mia, S) => S != summer)).

% 5. James wants to have a long vacation.
fof(james_wants, axiom, wants_long_vacation(james)).

% Negated conclusion: Mia's favorite season is NOT spring.
fof(neg_conclusion, conjecture, ~favorite_season(mia, spring)).