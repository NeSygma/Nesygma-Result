fof(p1, axiom, ! [F] : (appropriate_for_all_ages(F) => can_watch_without_guidance(F))).
fof(p2, axiom, ! [F] : (excessive_erotic_violent(F) => ~can_watch_without_guidance(F))).
fof(p3, axiom, ! [F] : (rated_ga(F) => appropriate_for_all_ages(F))).
fof(p4, axiom, ! [F] : (family_friendly_animated(F) => rated_ga(F))).
fof(p5, axiom, ! [F] : (in_frozen_series(F) => family_friendly_animated(F))).
fof(p6, axiom, film(hachi)).
fof(p7, axiom, (family_friendly_animated(hachi) | appropriate_for_all_ages(hachi))).
fof(goal, conjecture, rated_ga(hachi)).