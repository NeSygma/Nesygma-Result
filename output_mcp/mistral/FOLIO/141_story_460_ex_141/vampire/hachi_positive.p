fof(all_ages_implies_watchable, axiom, 
    ! [F] : (all_ages(F) => can_watch_without_guidance(F))).

fof(excessive_content_implies_not_watchable, axiom, 
    ! [F] : (excessive_content(F) => ~can_watch_without_guidance(F))).

fof(rated_general_audience_implies_all_ages, axiom, 
    ! [F] : (rated_general_audience(F) => all_ages(F))).

fof(family_friendly_animated_implies_rated_general, axiom, 
    ! [F] : (family_friendly_animated(F) => rated_general_audience(F))).

fof(frozen_series_implies_family_friendly_animated, axiom, 
    ! [F] : (frozen_series(F) => family_friendly_animated(F))).

fof(hachi_is_film, axiom, 
    film(hachi_dog_tale)).

fof(hachi_either_family_friendly_or_all_ages, axiom, 
    family_friendly_animated(hachi_dog_tale) | all_ages(hachi_dog_tale)).

fof(conclusion, conjecture, 
    excessive_content(hachi_dog_tale) | frozen_series(hachi_dog_tale)).