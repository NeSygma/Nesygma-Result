% Positive version: original conclusion as conjecture
% Conclusion: "Hachi: A dog's Tale" contains excessive erotic and violent content or is in the "Frozen" series or both.

% Predicates:
% appropriate_all_ages(X) - film X is appropriate for people of all ages
% can_watch_no_guidance(X) - children can watch X without guidance from parents
% contains_excessive(X) - film X contains excessive erotic and violent content
% rated_general_audience(X) - film X is rated General Audience
% family_friendly_animated(X) - film X is a family-friendly animated film
% frozen_series(X) - film X is in the Frozen series
% film(X) - X is a film

% Constants:
% hachi - "Hachi: A dog's Tale"

fof(distinct, axiom, $true). % No distinctness needed for single constant

% Premise 1: If a film is appropriate for people of all ages, then children can watch it without guidance from parents.
fof(premise1, axiom, ! [X] : (appropriate_all_ages(X) => can_watch_no_guidance(X))).

% Premise 2: If a film contains excessive erotic and violent content, children cannot watch it without guidance from their parents.
fof(premise2, axiom, ! [X] : (contains_excessive(X) => ~can_watch_no_guidance(X))).

% Premise 3: If a film is rated General Audience, then it is appropriate for people of all ages.
fof(premise3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).

% Premise 4: All family-friendly animated films are rated General Audience.
fof(premise4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).

% Premise 5: All movies in the Frozen series are family-friendly animated films.
fof(premise5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).

% Premise 6: "Hachi: A dog's Tale" is a film.
fof(premise6, axiom, film(hachi)).

% Premise 7: "Hachi: A dog's Tale" is either a family-friendly animated film or is appropriate for people of all ages.
fof(premise7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).

% Conclusion: "Hachi: A dog's Tale" contains excessive erotic and violent content or is in the "Frozen" series or both.
fof(conclusion, conjecture, contains_excessive(hachi) | frozen_series(hachi)).