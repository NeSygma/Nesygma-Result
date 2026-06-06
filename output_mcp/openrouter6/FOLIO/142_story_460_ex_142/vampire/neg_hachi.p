fof(premise1, axiom, ! [X] : (appropriate_all_ages(X) => children_can_watch(X))).
fof(premise2, axiom, ! [X] : (contains_excessive(X) => children_cannot_watch(X))).
fof(premise3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).
fof(premise4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).
fof(premise5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).
fof(premise6, axiom, film(hachi)).
fof(premise7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).
fof(neg_conclusion, conjecture, ~((contains_excessive(hachi) & frozen_series(hachi)) | (~contains_excessive(hachi) & ~frozen_series(hachi)))).