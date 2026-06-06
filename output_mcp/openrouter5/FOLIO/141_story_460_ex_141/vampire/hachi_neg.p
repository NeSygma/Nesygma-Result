% Negative version: negated conclusion as conjecture
% Negated conclusion: NOT (contains_excessive(hachi) | frozen_series(hachi))
% i.e., ~contains_excessive(hachi) & ~frozen_series(hachi)

fof(distinct, axiom, $true).

% Premise 1
fof(premise1, axiom, ! [X] : (appropriate_all_ages(X) => can_watch_no_guidance(X))).

% Premise 2
fof(premise2, axiom, ! [X] : (contains_excessive(X) => ~can_watch_no_guidance(X))).

% Premise 3
fof(premise3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).

% Premise 4
fof(premise4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).

% Premise 5
fof(premise5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).

% Premise 6
fof(premise6, axiom, film(hachi)).

% Premise 7
fof(premise7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).

% Negated conclusion: hachi does NOT contain excessive content AND is NOT in the Frozen series
fof(neg_conclusion, conjecture, ~contains_excessive(hachi) & ~frozen_series(hachi)).