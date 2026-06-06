fof(p1, axiom, ! [X] : (appropriate_all_ages(X) => can_watch_without_guidance(X))).
fof(p2, axiom, ! [X] : (excessive_erotic_violent(X) => ~can_watch_without_guidance(X))).
fof(p3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).
fof(p4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).
fof(p5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).
fof(p6, axiom, film(hachi)).
fof(p7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).
fof(goal, conjecture, rated_general_audience(hachi)).