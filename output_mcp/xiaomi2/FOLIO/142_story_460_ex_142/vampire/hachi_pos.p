fof(appropriate_implies_watch, axiom,
    ! [X] : (appropriate_all_ages(X) => can_watch_without_guidance(X))).

fof(excessive_implies_not_watch, axiom,
    ! [X] : (excessive_erotic_violent(X) => ~can_watch_without_guidance(X))).

fof(rated_ga_implies_appropriate, axiom,
    ! [X] : (rated_general_audience(X) => appropriate_all_ages(X))).

fof(family_friendly_implies_rated_ga, axiom,
    ! [X] : (family_friendly_animated(X) => rated_general_audience(X))).

fof(frozen_implies_family_friendly, axiom,
    ! [X] : (frozen_series(X) => family_friendly_animated(X))).

fof(hachi_is_film, axiom,
    film(hachi)).

fof(hachi_family_or_appropriate, axiom,
    family_friendly_animated(hachi) | appropriate_all_ages(hachi)).

fof(conclusion, conjecture,
    (excessive_erotic_violent(hachi) & frozen_series(hachi))
    | (~excessive_erotic_violent(hachi) & ~frozen_series(hachi))).