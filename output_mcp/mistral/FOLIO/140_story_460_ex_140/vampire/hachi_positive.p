fof(all_ages_implies_watchable, axiom, 
    ! [F] : (all_ages_appropriate(F) => can_watch_without_guidance(F))).

fof(excessive_content_implies_not_watchable, axiom, 
    ! [F] : (excessive_content(F) => ~can_watch_without_guidance(F))).

fof(general_audience_implies_all_ages, axiom, 
    ! [F] : (rated_general_audience(F) => all_ages_appropriate(F))).

fof(family_friendly_animated_implies_general_audience, axiom, 
    ! [F] : (family_friendly_animated(F) => rated_general_audience(F))).

fof(frozen_series_implies_family_friendly_animated, axiom, 
    ! [F] : (frozen_series(F) => family_friendly_animated(F))).

fof(hachi_is_film, axiom, 
    film(hachi)).

fof(hachi_is_family_friendly_or_all_ages, axiom, 
    (family_friendly_animated(hachi) | all_ages_appropriate(hachi))).

fof(goal, conjecture, 
    rated_general_audience(hachi)).