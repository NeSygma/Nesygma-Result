fof(premise1, axiom, ! [X] : (rated_ga(X) => appropriate_for_all_ages(X))).
fof(premise2, axiom, ! [X] : (family_friendly_animated(X) => rated_ga(X))).
fof(premise3, axiom, ! [X] : (in_frozen_series(X) => family_friendly_animated(X))).
fof(premise4, axiom, ! [X] : (appropriate_for_all_ages(X) => can_watch_without_parent_guidance(X))).
fof(premise5, axiom, ! [X] : (contains_excessive_erotic_violent(X) => ~can_watch_without_parent_guidance(X))).
fof(fact_film, axiom, film(hachi_dog_s_tale)).
fof(disjunction, axiom, (family_friendly_animated(hachi_dog_s_tale) | appropriate_for_all_ages(hachi_dog_s_tale))).
fof(conjecture, conjecture, rated_ga(hachi_dog_s_tale)).