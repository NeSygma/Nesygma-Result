fof(p1, axiom, ! [X] : ((film(X) & appropriate_all_ages(X)) => children_watch_no_guidance(X))).
fof(p2, axiom, ! [X] : ((film(X) & contains_excessive_erotic_violent(X)) => ~children_watch_no_guidance(X))).
fof(p3, axiom, ! [X] : ((film(X) & rated_general_audience(X)) => appropriate_all_ages(X))).
fof(p4, axiom, ! [X] : ((film(X) & family_friendly_animated(X)) => rated_general_audience(X))).
fof(p5, axiom, ! [X] : ((film(X) & frozen_series(X)) => family_friendly_animated(X))).
fof(p6, axiom, film(hachi)).
fof(p7, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).
fof(neg_goal, conjecture, ~(contains_excessive_erotic_violent(hachi) | frozen_series(hachi))).