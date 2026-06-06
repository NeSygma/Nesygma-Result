fof(premise1, axiom, ! [X] : (appropriate_all_ages(X) => can_watch_without_guidance(X))).
fof(premise2, axiom, ! [X] : (excessive_erotic_violent(X) => ~can_watch_without_guidance(X))).
fof(premise3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).
fof(premise4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).
fof(premise5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).
fof(premise6, axiom, film(hachi)).
fof(premise7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).
fof(goal, conjecture, ~(excessive_erotic_violent(hachi) | frozen_series(hachi))).