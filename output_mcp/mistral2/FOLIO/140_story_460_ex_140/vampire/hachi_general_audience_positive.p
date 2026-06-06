fof(axiom_1, axiom,
    ! [Film] : (appropriate_for_all_ages(Film) => can_watch_without_guidance(Film))).

fof(axiom_2, axiom,
    ! [Film] : (excessive_erotic_violent_content(Film) => ~can_watch_without_guidance(Film))).

fof(axiom_3, axiom,
    ! [Film] : (rated_general_audience(Film) => appropriate_for_all_ages(Film))).

fof(axiom_4, axiom,
    ! [Film] : (family_friendly_animated(Film) => rated_general_audience(Film))).

fof(axiom_5, axiom,
    ! [Film] : (frozen_series_movie(Film) => family_friendly_animated(Film))).

fof(fact_1, axiom,
    film(hachi_a_dogs_tale)).

fof(fact_2, axiom,
    family_friendly_animated(hachi_a_dogs_tale) | appropriate_for_all_ages(hachi_a_dogs_tale)).

fof(conclusion, conjecture,
    rated_general_audience(hachi_a_dogs_tale)).