% Positive: Premises + conclusion as conjecture
fof(premise_1, axiom, ! [X] : (appropriate_for_all_ages(X) => children_can_watch_without_guidance(X))).
fof(premise_2, axiom, ! [X] : (contains_excessive_content(X) => ~children_can_watch_without_guidance(X))).
fof(premise_3, axiom, ! [X] : (rated_general_audience(X) => appropriate_for_all_ages(X))).
fof(premise_4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).
fof(premise_5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).
fof(premise_6, axiom, film(hachi)).
fof(premise_7, axiom, family_friendly_animated(hachi) | appropriate_for_all_ages(hachi)).
fof(conclusion, conjecture, rated_general_audience(hachi)).