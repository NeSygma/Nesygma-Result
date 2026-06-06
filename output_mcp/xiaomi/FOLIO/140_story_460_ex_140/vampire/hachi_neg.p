fof(film_hachi, axiom, film(hachi)).

fof(premise_1, axiom, ! [X] : (appropriate_all_ages(X) => can_watch_without_guidance(X))).

fof(premise_2, axiom, ! [X] : (excessive_erotic_violent(X) => ~can_watch_without_guidance(X))).

fof(premise_3, axiom, ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).

fof(premise_4, axiom, ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).

fof(premise_5, axiom, ! [X] : (frozen_series(X) => family_friendly_animated(X))).

fof(premise_6, axiom, family_friendly_animated(hachi) | appropriate_all_ages(hachi)).

fof(goal, conjecture, ~rated_general_audience(hachi)).