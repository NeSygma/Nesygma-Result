fof(premise1, axiom, ! [X] : ((film(X) & appropriate_all_ages(X)) => can_watch_no_guidance(X))).
fof(premise2, axiom, ! [X] : ((film(X) & contains_excessive_ev(X)) => ~can_watch_no_guidance(X))).
fof(premise3, axiom, ! [X] : ((film(X) & rated_general_audience(X)) => appropriate_all_ages(X))).
fof(premise4, axiom, ! [X] : ((film(X) & family_friendly_animated(X)) => rated_general_audience(X))).
fof(premise5, axiom, ! [X] : ((film(X) & frozen_series(X)) => family_friendly_animated(X))).
fof(premise6, axiom, film(hachi)).
fof(premise7, axiom, (family_friendly_animated(hachi) | appropriate_all_ages(hachi))).
fof(distinct, axiom, $true).
fof(conclusion, conjecture, 
    ((contains_excessive_ev(hachi) & frozen_series(hachi)) | (~contains_excessive_ev(hachi) & ~frozen_series(hachi)))).