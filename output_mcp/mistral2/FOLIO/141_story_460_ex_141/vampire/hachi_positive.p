fof(premise1, axiom, 
    ! [F] : (appropriate_for_all_ages(F) => children_can_watch_without_guidance(F))).

fof(premise2, axiom, 
    ! [F] : (excessive_erotic_violent_content(F) => cannot_watch_without_guidance(F))).

fof(premise3, axiom, 
    ! [F] : (rated_general_audience(F) => appropriate_for_all_ages(F))).

fof(premise4, axiom, 
    ! [F] : (family_friendly_animated(F) => rated_general_audience(F))).

fof(premise5, axiom, 
    ! [F] : (in_frozen_series(F) => family_friendly_animated(F))).

fof(premise6, axiom, 
    family_friendly_animated(hachi_a_dogs_tale) | appropriate_for_all_ages(hachi_a_dogs_tale)).

fof(goal, conjecture, 
    excessive_erotic_violent_content(hachi_a_dogs_tale) |
    in_frozen_series(hachi_a_dogs_tale)).