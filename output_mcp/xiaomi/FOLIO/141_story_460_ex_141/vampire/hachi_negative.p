fof(premise_1, axiom, ! [F] : (appropriate_all_ages(F) => children_can_watch_without_guidance(F))).
fof(premise_2, axiom, ! [F] : (excessive_erotic_violent(F) => ~children_can_watch_without_guidance(F))).
fof(premise_3, axiom, ! [F] : (rated_general_audience(F) => appropriate_all_ages(F))).
fof(premise_4, axiom, ! [F] : (family_friendly_animated(F) => rated_general_audience(F))).
fof(premise_5, axiom, ! [F] : (in_frozen_series(F) => family_friendly_animated(F))).
fof(premise_6, axiom, film(hachi)).
fof(premise_7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).
fof(goal, conjecture, ~(excessive_erotic_violent(hachi) | in_frozen_series(hachi))).