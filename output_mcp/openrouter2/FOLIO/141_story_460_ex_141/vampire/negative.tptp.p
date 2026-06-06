fof(imp1, axiom, ! [X] : ((appropriate_for_all_ages(X) => children_can_watch_without_parent_guidance(X)))).
fof(imp2, axiom, ! [X] : ((contains_excessive_erotic_and_violent_content(X) => ~children_can_watch_without_parent_guidance(X)))).
fof(imp3, axiom, ! [X] : ((rated_general_audience(X) => appropriate_for_all_ages(X)))).
fof(imp4, axiom, ! [X] : ((family_friendly_animated_film(X) => rated_general_audience(X)))).
fof(imp5, axiom, ! [X] : ((in_frozen_series(X) => family_friendly_animated_film(X)))).
fof(film_hachi, axiom, film(hachi)).
fof(disj, axiom, (family_friendly_animated_film(hachi) | appropriate_for_all_ages(hachi))).
fof(conjecture, conjecture, (~contains_excessive_erotic_and_violent_content(hachi) & ~in_frozen_series(hachi))).