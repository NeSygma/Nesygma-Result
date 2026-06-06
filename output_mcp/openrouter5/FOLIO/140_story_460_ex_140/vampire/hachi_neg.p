% Negative version: claim is "Hachi is NOT rated General Audience"
fof(distinct, axiom, (hachi != frozen_1 & hachi != frozen_2 & frozen_1 != frozen_2)).

% Predicates:
% appropriate_all_ages(X) - film X is appropriate for people of all ages
% can_watch_no_guidance(X) - children can watch X without parental guidance
% contains_excessive_erotic_violent(X) - film X contains excessive erotic and violent content
% rated_general_audience(X) - film X is rated General Audience
% family_friendly_animated(X) - film X is a family-friendly animated film
% frozen_series(X) - film X is in the Frozen series
% film(X) - X is a film

fof(premise_1, axiom, ! [X] : (appropriate_all_ages(X) => can_watch_no_guidance(X))).
fof(premise_2, axiom, ! [X] : (contains_excessive_erotic_violent(X) => ~can_watch_no_guidance(X))).
fof(premise_3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).
fof(premise_4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).
fof(premise_5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).
fof(premise_6, axiom, film(hachi)).
fof(premise_7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).

fof(goal, conjecture, ~rated_general_audience(hachi)).