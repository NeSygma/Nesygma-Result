fof(premise1, axiom,
    ! [Film] : (appropriate_for_all_ages(Film) => children_can_watch_without_guidance(Film))).

fof(premise2, axiom,
    ! [Film] : (contains_excessive_erotic_violent_content(Film) => children_cannot_watch_without_guidance(Film))).

fof(premise3, axiom,
    ! [Film] : (rated_general_audience(Film) => appropriate_for_all_ages(Film))).

fof(premise4, axiom,
    ! [Film] : (family_friendly_animated_film(Film) => rated_general_audience(Film))).

fof(premise5, axiom,
    ! [Film] : (film_in_frozen_series(Film) => family_friendly_animated_film(Film))).

fof(premise6, axiom,
    film(hachi_a_dogs_tale)).

fof(premise7, axiom,
    family_friendly_animated_film(hachi_a_dogs_tale) |
    appropriate_for_all_ages(hachi_a_dogs_tale)).

fof(conclusion, conjecture,
    (contains_excessive_erotic_violent_content(hachi_a_dogs_tale) &
     film_in_frozen_series(hachi_a_dogs_tale)) |
    (~contains_excessive_erotic_violent_content(hachi_a_dogs_tale) &
     ~film_in_frozen_series(hachi_a_dogs_tale))).