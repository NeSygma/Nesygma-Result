% Premises about films and content
fof(premise_1, axiom, ! [X] : (appropriate_for_all_ages(X) => children_can_watch_without_guidance(X))).
fof(premise_2, axiom, ! [X] : (contains_excessive_content(X) => children_need_guidance(X))).
fof(premise_3, axiom, ! [X] : (rated_general_audience(X) => appropriate_for_all_ages(X))).
fof(premise_4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).
fof(premise_5, axiom, ! [X] : (in_frozen_series(X) => family_friendly_animated(X))).
fof(premise_6, axiom, film(hachi)).
fof(premise_7, axiom, (family_friendly_animated(hachi) | appropriate_for_all_ages(hachi))).

% Negated conclusion
fof(negated_conclusion, conjecture, ~(contains_excessive_content(hachi) | in_frozen_series(hachi))).